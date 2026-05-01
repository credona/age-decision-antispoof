import json
import logging
from datetime import UTC, datetime
from typing import Any

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
    """Log a structured JSON event.

    Logs must remain machine-readable and must never contain raw image data.
    """
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "service": project_metadata.service_name,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
        "event": event,
        **(payload or {}),
    }

    message = json.dumps(log_entry, ensure_ascii=False, sort_keys=True)

    if level == "error":
        logger.error(message)
        return

    if level == "warning":
        logger.warning(message)
        return

    logger.info(message)
