import json
import logging
from datetime import UTC, datetime
from typing import Any

from antispoof.domain.privacy.safe_logging import sanitize_log_payload
from antispoof.project import project_metadata

logger = logging.getLogger("antispoof")
logger.setLevel(logging.INFO)
logger.propagate = False

handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)


def log_event(
    event: str,
    payload: dict[str, Any] | None = None,
    level: str = "info",
) -> None:
    """Log a structured privacy-safe JSON event."""
    safe_payload = sanitize_log_payload(payload or {})

    log_entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "service": project_metadata.service_name,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
        "event": event,
        **safe_payload,
    }

    message = json.dumps(log_entry, ensure_ascii=False, sort_keys=True)

    if level == "error":
        logger.error(message)
        return

    if level == "warning":
        logger.warning(message)
        return

    logger.info(message)
