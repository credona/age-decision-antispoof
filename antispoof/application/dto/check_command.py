from dataclasses import dataclass


@dataclass(frozen=True)
class CheckCommand:
    image_bytes: bytes
    request_id: str
    correlation_id: str
