import hashlib
import hmac


class Sha256CalibrationIntegrityVerifier:
    def verify(self, *, payload: bytes, expected_hash: str) -> bool:
        if not expected_hash.startswith("sha256:"):
            return False

        expected_digest = expected_hash.removeprefix("sha256:")
        actual_digest = hashlib.sha256(payload).hexdigest()

        return hmac.compare_digest(actual_digest, expected_digest)
