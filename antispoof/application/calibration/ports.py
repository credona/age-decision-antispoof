from typing import Protocol


class CalibrationPolicyReaderPort(Protocol):
    def read_policy_bytes(self) -> bytes: ...


class CalibrationIntegrityVerifierPort(Protocol):
    def verify(self, *, payload: bytes, expected_hash: str) -> bool: ...


class CalibrationSignatureVerifierPort(Protocol):
    def verify(self, *, payload: bytes, signature: str) -> bool: ...
