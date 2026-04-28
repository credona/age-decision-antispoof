from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class RequestContext:
    """Carries request identifiers across API responses and logs."""

    request_id: str
    correlation_id: str


def build_request_context(
    request_id: str | None = None,
    correlation_id: str | None = None,
) -> RequestContext:
    """Build a request context from incoming headers or generated identifiers."""
    resolved_request_id = request_id or str(uuid4())
    resolved_correlation_id = correlation_id or resolved_request_id

    return RequestContext(
        request_id=resolved_request_id,
        correlation_id=resolved_correlation_id,
    )
