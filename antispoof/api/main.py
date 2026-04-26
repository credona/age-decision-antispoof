import os

import cv2
import numpy as np
from fastapi import FastAPI, File, Header, HTTPException, UploadFile

from antispoof import AntiSpoof
from antispoof.core import build_request_context
from antispoof.exceptions import AntiSpoofError
from antispoof.models.loader import AntiSpoofModelLoader
from antispoof.privacy import build_privacy_metadata
from antispoof.utils.logger import log_event
from antispoof.benchmark import run_local_benchmark

APP_NAME = os.getenv("APP_NAME", "Age Decision AntiSpoof")
APP_VERSION = os.getenv("APP_VERSION", "1.1.0")

THRESHOLD = float(os.getenv("ANTISPOOF_THRESHOLD", "0.5"))

MODEL_WEIGHT = float(os.getenv("MODEL_WEIGHT", "0.7"))
TEXTURE_WEIGHT = float(os.getenv("TEXTURE_WEIGHT", "0.15"))
SCREEN_WEIGHT = float(os.getenv("SCREEN_WEIGHT", "0.15"))

PROVIDER = "age-decision-antispoof"
MODEL_NAME = "MiniFASNetV2"
MODEL_TYPE = "onnx"
HEURISTICS = [
    "texture",
    "screen_pattern",
    "blur",
]


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)


model_loader = AntiSpoofModelLoader()

pipeline = AntiSpoof(
    threshold=THRESHOLD,
    model_weight=MODEL_WEIGHT,
    texture_weight=TEXTURE_WEIGHT,
    screen_weight=SCREEN_WEIGHT,
)


@app.get("/health")
def health():
    """Return service health status."""
    return {
        "status": "ok",
        "service": PROVIDER,
        "version": APP_VERSION,
    }


@app.get("/model/status")
def model_status():
    """Return anti-spoofing model and heuristic status."""
    model_metadata = model_loader.status()

    return {
        "service": PROVIDER,
        "version": APP_VERSION,
        "antispoof_model": {
            **model_metadata,
            "loaded": True,
        },
        "heuristics": HEURISTICS,
        "threshold": THRESHOLD,
        "weights": {
            "model": MODEL_WEIGHT,
            "texture": TEXTURE_WEIGHT,
            "screen": SCREEN_WEIGHT,
        },
    }

@app.get("/benchmark")
def benchmark(
    x_request_id: str | None = Header(default=None, alias="X-Request-ID"),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
):
    """Run local benchmark evaluation and expose PAD metrics."""
    context = build_request_context(
        request_id=x_request_id,
        correlation_id=x_correlation_id,
    )

    try:
        result = run_local_benchmark()

        response = {
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "provider": PROVIDER,
            **result,
        }

        log_event(
            "antispoof_benchmark_completed",
            {
                "request_id": context.request_id,
                "correlation_id": context.correlation_id,
                "provider": PROVIDER,
                "sample_count": response["dataset"]["sample_count"],
                "current_threshold": response["current_threshold"],
                "recommended_threshold": response["threshold_tuning"]["recommended_threshold"],
                "apcer": response["metrics"]["apcer"],
                "bpcer": response["metrics"]["bpcer"],
                "acer": response["metrics"]["acer"],
                "tuned_apcer": response["threshold_tuning"]["metrics"]["apcer"],
                "tuned_bpcer": response["threshold_tuning"]["metrics"]["bpcer"],
                "tuned_acer": response["threshold_tuning"]["metrics"]["acer"],
            },
        )

        return response

    except FileNotFoundError as exc:
        log_event(
            "antispoof_benchmark_unavailable",
            {
                "request_id": context.request_id,
                "correlation_id": context.correlation_id,
                "error": str(exc),
            },
            level="warning",
        )
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/check")
async def check(
    file: UploadFile = File(...),
    x_request_id: str | None = Header(default=None, alias="X-Request-ID"),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
):
    """Run anti-spoofing verification on an uploaded image.

    The image is processed in memory only and is never persisted.
    """
    context = build_request_context(
        request_id=x_request_id,
        correlation_id=x_correlation_id,
    )

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(status_code=400, detail="Empty image file")

        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        result = pipeline.predict(image)

        response = {
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "provider": PROVIDER,
            "decision": result.label,
            "is_real": result.is_real,
            "spoof_detected": not result.is_real,
            "confidence": result.confidence,
            "spoof_score": result.spoof_score,
            "cred_antispoof_score": result.cred_antispoof_score,
            "threshold": result.threshold,
            "rejection_reason": None,
            "privacy": build_privacy_metadata(),
            "model_info": {
                "antispoof_model": MODEL_NAME,
                "model_type": MODEL_TYPE,
                "heuristics": HEURISTICS,
            },
            "details": result.details,
        }

        log_event(
            "antispoof_check_completed",
            {
                "request_id": context.request_id,
                "correlation_id": context.correlation_id,
                "decision": response["decision"],
                "is_real": response["is_real"],
                "spoof_detected": response["spoof_detected"],
                "confidence": response["confidence"],
                "spoof_score": response["spoof_score"],
                "cred_antispoof_score": response["cred_antispoof_score"],
                "threshold": response["threshold"],
                "provider": response["provider"],
                "image_persisted": response["privacy"]["image_persisted"],
                "raw_image_logged": response["privacy"]["raw_image_logged"],
            },
        )

        return response

    except HTTPException as exc:
        log_event(
            "antispoof_check_rejected",
            {
                "request_id": context.request_id,
                "correlation_id": context.correlation_id,
                "status_code": exc.status_code,
                "detail": exc.detail,
            },
            level="warning",
        )
        raise

    except AntiSpoofError as exc:
        log_event(
            "antispoof_check_failed",
            {
                "request_id": context.request_id,
                "correlation_id": context.correlation_id,
                "error": str(exc),
            },
            level="warning",
        )
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        log_event(
            "antispoof_check_failed",
            {
                "request_id": context.request_id,
                "correlation_id": context.correlation_id,
                "error": "internal_error",
            },
            level="error",
        )
        raise HTTPException(status_code=500, detail="Internal error") from exc