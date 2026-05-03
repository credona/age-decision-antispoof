PUBLIC_CHECK_RESPONSE_FIELDS = {
    "request_id",
    "correlation_id",
    "provider",
    "decision",
    "is_real",
    "spoof_detected",
    "cred_antispoof_score",
    "rejection_reason",
    "privacy",
    "engine_info",
}


def filter_check_response(payload: dict) -> dict:
    """
    Public API contract barrier.

    Any internal score, model detail, heuristic output or raw value not declared
    in the public check response contract is ignored here.
    """
    return {key: payload[key] for key in PUBLIC_CHECK_RESPONSE_FIELDS if key in payload}
