import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from antispoof.domain.calibration import CalibrationActivationError


class Ed25519CalibrationSignatureVerifier:
    def __init__(self, public_key_b64: str | None):
        self.public_key_b64 = public_key_b64

    def verify(self, *, payload: bytes, signature: str) -> bool:
        if not self.public_key_b64:
            raise CalibrationActivationError("CALIBRATION_PUBLIC_KEY_MISSING")

        try:
            public_key = Ed25519PublicKey.from_public_bytes(base64.b64decode(self.public_key_b64))
            public_key.verify(base64.b64decode(signature), payload)
            return True
        except (ValueError, InvalidSignature):
            return False
