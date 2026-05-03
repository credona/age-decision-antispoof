import os

from fastapi import FastAPI, File, Header, Query, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from antispoof import AntiSpoof
from antispoof.api.input_validator import UnsupportedInputTypeError, validate_input_type
from antispoof.api.response_filter import filter_check_response
from antispoof.api.schemas import ErrorResponse
from antispoof.application.dto.check_command import CheckCommand
from antispoof.application.use_cases.run_spoof_check import RunSpoofCheckUseCase
from antispoof.benchmark import run_local_benchmark
from antispoof.core import build_request_context
from antispoof.domain.constants import (
    LOG_LEVEL_ERROR,
    LOG_LEVEL_WARNING,
    MODEL_NAME_MINIFASNET,
    MODEL_TYPE_ONNX,
    STATUS_OK,
)
from antispoof.domain.privacy import build_privacy_metadata
from antispoof.exceptions import AntiSpoofError
from antispoof.infrastructure.logging.safe_logger import log_event
from antispoof.infrastructure.models.loader import AntiSpoofModelLoader
from antispoof.project import project_metadata

THRESHOLD = float(os.getenv("ANTISPOOF_THRESHOLD", "0.5"))

MODEL_WEIGHT = float(os.getenv("MODEL_WEIGHT", "0.7"))
TEXTURE_WEIGHT = float(os.getenv("TEXTURE_WEIGHT", "0.15"))
SCREEN_WEIGHT = float(os.getenv("SCREEN_WEIGHT", "0.15"))

PROVIDER = project_metadata.service_name
MODEL_NAME = MODEL_NAME_MINIFASNET
MODEL_TYPE = MODEL_TYPE_ONNX
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
run_spoof_check_use_case = RunSpoofCheckUseCase(pipeline)


@app.get("/health")
def health():
    """Return service health status."""
    return {
        "status": STATUS_OK,
        "service": project_metadata.service_name,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
    }


@app.get("/version")
def version():
    """Return service version metadata."""
    return project_metadata.model_dump()


@app.get("/engine/status")
def engine_status():
    """Return spoof check engine status."""
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
            level=LOG_LEVEL_WARNING,
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
            level=LOG_LEVEL_ERROR,
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
    input_type: str = Query(default="image"),
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
        validate_input_type(input_type)

        contents = await file.read()

        if not contents:
            return _rejected_check_response(
                request_id=context.request_id,
                correlation_id=context.correlation_id,
                code="empty_file",
            )

        result = run_spoof_check_use_case.execute(
            CheckCommand(
                image_bytes=contents,
                request_id=context.request_id,
                correlation_id=context.correlation_id,
            )
        )

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
            "engine_info": {
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

        return filter_check_response(response)

    except UnsupportedInputTypeError as exc:
        _log_error(
            event="antispoof_check_rejected",
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            error_type="validation_error",
            error_code="UNSUPPORTED_INPUT_TYPE",
            level=LOG_LEVEL_WARNING,
        )

        return _error_response(
            status_code=400,
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            code="UNSUPPORTED_INPUT_TYPE",
            message=str(exc),
        )

    except ValueError:
        _log_error(
            event="antispoof_check_rejected",
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            error_type="validation_error",
            error_code="invalid_image",
            level=LOG_LEVEL_WARNING,
        )

        return _error_response(
            status_code=400,
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            code="invalid_image",
            message="Invalid request.",
        )

    except AntiSpoofError:
        _log_error(
            event="antispoof_check_failed",
            request_id=context.request_id,
            correlation_id=context.correlation_id,
            error_type="antispoof_error",
            error_code="antispoof_processing_error",
            level=LOG_LEVEL_WARNING,
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
            level=LOG_LEVEL_ERROR,
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
        level=LOG_LEVEL_WARNING,
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
        level=LOG_LEVEL_WARNING,
    )

    return _error_response(
        status_code=400,
        request_id=context.request_id,
        correlation_id=context.correlation_id,
        code=error_code,
        message="Invalid request.",
    )


app.add_exception_handler(RequestValidationError, handle_request_validation_error)
