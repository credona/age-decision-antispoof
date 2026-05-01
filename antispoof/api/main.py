import os

import cv2
import numpy as np
from fastapi import FastAPI, File, Header, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from antispoof import AntiSpoof
from antispoof.api.schemas import ErrorResponse
from antispoof.benchmark import run_local_benchmark
from antispoof.core import build_request_context
from antispoof.exceptions import AntiSpoofError
from antispoof.models.loader import AntiSpoofModelLoader
from antispoof.privacy import build_privacy_metadata
from antispoof.project import project_metadata
from antispoof.utils.logger import log_event

THRESHOLD = float(os.getenv("ANTISPOOF_THRESHOLD", "0.5"))

MODEL_WEIGHT = float(os.getenv("MODEL_WEIGHT", "0.7"))
TEXTURE_WEIGHT = float(os.getenv("TEXTURE_WEIGHT", "0.15"))
SCREEN_WEIGHT = float(os.getenv("SCREEN_WEIGHT", "0.15"))

PROVIDER = project_metadata.service_name
MODEL_NAME = "MiniFASNetV2"
MODEL_TYPE = "onnx"
HEURISTICS = [
    "texture",
    "screen_pattern",
    "blur",
]

app = FastAPI(
    title=project_metadata.app_name,
    version=project_metadata.version,
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
        "service": project_metadata.service_name,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
    }


@app.get("/version")
def version():
    """Return service version metadata."""
    return project_metadata.model_dump()


@app.get("/model/status")
def model_status():
    """Return anti-spoofing model and heuristic status."""
    model_metadata = model_loader.status()

    return {
        "service": PROVIDER,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
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


@app.get(
    "/benchmark",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
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

    except FileNotFoundError:
        _log_error(
            event="antispoof_benchmark_unavailable",
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            error_type="dataset_error",
            error_code="benchmark_dataset_unavailable",
            level="warning",
        )

        return _error_response(
            status_code=404,
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            code="benchmark_dataset_unavailable",
            message="Benchmark dataset unavailable.",
        )

    except Exception:
        _log_error(
            event="antispoof_benchmark_failed",
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            error_type="runtime_error",
            error_code="benchmark_runtime_error",
            level="error",
        )

        return _error_response(
            status_code=500,
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            code="benchmark_runtime_error",
            message="An internal error has occurred.",
        )


@app.post(
    "/check",
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def check(
    file: UploadFile = File(...),
    x_request_id: str | None = Header(default=None, alias="X-Request-ID"),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
):
    """Run anti-spoofing verification on an uploaded image.

    The image is processed in memory only and is never persisted.
    Internal model scores and heuristic details are not exposed publicly.
    """
    context = build_request_context(
        request_id=x_request_id,
        correlation_id=x_correlation_id,
    )

    try:
        contents = await file.read()

        if not contents:
            return _rejected_check_response(
                request_id=context.request_id,
                correlation_id=context.correlation_id,
                code="empty_file",
            )

        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return _rejected_check_response(
                request_id=context.request_id,
                correlation_id=context.correlation_id,
                code="invalid_image",
            )

        result = pipeline.predict(image)

        response = {
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "provider": PROVIDER,
            "decision": result.label,
            "is_real": result.is_real,
            "spoof_detected": not result.is_real,
            "cred_antispoof_score": result.cred_antispoof_score,
            "rejection_reason": None,
            "privacy": build_privacy_metadata(),
            "model_info": {
                "antispoof_model": MODEL_NAME,
                "model_type": MODEL_TYPE,
                "heuristics": HEURISTICS,
            },
        }

        log_event(
            "antispoof_check_completed",
            {
                "request_id": context.request_id,
                "correlation_id": context.correlation_id,
                "decision": response["decision"],
                "is_real": response["is_real"],
                "spoof_detected": response["spoof_detected"],
                "cred_antispoof_score": response["cred_antispoof_score"],
                "provider": response["provider"],
                "image_persisted": response["privacy"]["image_persisted"],
                "raw_image_logged": response["privacy"]["raw_image_logged"],
            },
        )

        return response

    except AntiSpoofError:
        _log_error(
            event="antispoof_check_failed",
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            error_type="antispoof_error",
            error_code="antispoof_processing_error",
            level="warning",
        )

        return _error_response(
            status_code=400,
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            code="antispoof_processing_error",
            message="Invalid request.",
        )

    except Exception:
        _log_error(
            event="antispoof_check_failed",
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            error_type="runtime_error",
            error_code="internal_error",
            level="error",
        )

        return _error_response(
            status_code=500,
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            code="internal_error",
            message="An internal error has occurred.",
        )


def _rejected_check_response(
    request_id: str,
    correlation_id: str,
    code: str,
) -> JSONResponse:
    _log_error(
        event="antispoof_check_rejected",
        request_id=request_id,
        correlation_id=correlation_id,
        error_type="validation_error",
        error_code=code,
        level="warning",
    )

    return _error_response(
        status_code=400,
        request_id=request_id,
        correlation_id=correlation_id,
        code=code,
        message="Invalid request.",
    )


def _error_response(
    status_code: int,
    request_id: str,
    correlation_id: str,
    code: str,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "request_id": request_id,
            "correlation_id": correlation_id,
            "error": {
                "code": code,
                "message": message,
            },
        },
    )


def _log_error(
    event: str,
    request_id: str,
    correlation_id: str,
    error_type: str,
    error_code: str,
    level: str,
) -> None:
    log_event(
        event,
        {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "error_type": error_type,
            "error_code": error_code,
        },
        level=level,
    )


def _map_validation_error_code(errors: list[dict]) -> str:
    for error in errors:
        loc = error.get("loc", ())
        error_type = error.get("type", "")

        if "file" in loc and error_type in {"missing", "value_error.missing"}:
            return "missing_file"

    return "invalid_request"


async def handle_request_validation_error(request: Request, exc: RequestValidationError):
    context = build_request_context(
        request_id=request.headers.get("x-request-id"),
        correlation_id=request.headers.get("x-correlation-id"),
    )
    error_code = _map_validation_error_code(exc.errors())

    _log_error(
        event="antispoof_check_rejected",
        request_id=context.request_id,
        correlation_id=context.correlation_id,
        error_type="validation_error",
        error_code=error_code,
        level="warning",
    )

    return _error_response(
        status_code=400,
        request_id=context.request_id,
        correlation_id=context.correlation_id,
        code=error_code,
        message="Invalid request.",
    )


app.add_exception_handler(RequestValidationError, handle_request_validation_error)
