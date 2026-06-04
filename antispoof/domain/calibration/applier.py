from dataclasses import dataclass

from antispoof.domain.calibration.policy import RuntimeCalibrationPolicy


@dataclass(frozen=True)
class CalibratedAntispoofSignal:
    final_score: float
    cred_antispoof_score: float


class AntispoofCalibrationApplier:
    def __init__(self, policy: RuntimeCalibrationPolicy | None = None):
        self.policy = policy

    def apply(
        self,
        *,
        final_score: float,
        cred_antispoof_score: float,
    ) -> CalibratedAntispoofSignal:
        if self.policy is None:
            return CalibratedAntispoofSignal(
                final_score=self._clamp_score(final_score),
                cred_antispoof_score=self._clamp_score(cred_antispoof_score),
            )

        parameters = self.policy.private_payload.get("calibration_parameters", {})

        final_score_offset = self._as_float(parameters.get("final_score_offset", 0.0))
        final_score_floor = self._as_float(parameters.get("final_score_floor", 0.0))
        final_score_ceiling = self._as_float(parameters.get("final_score_ceiling", 1.0))

        cred_score_offset = self._as_float(parameters.get("cred_antispoof_score_offset", 0.0))
        cred_score_floor = self._as_float(parameters.get("cred_antispoof_score_floor", 0.0))
        cred_score_ceiling = self._as_float(parameters.get("cred_antispoof_score_ceiling", 1.0))

        calibrated_final_score = self._clamp_score(final_score + final_score_offset)
        calibrated_final_score = max(calibrated_final_score, final_score_floor)
        calibrated_final_score = min(calibrated_final_score, final_score_ceiling)

        calibrated_cred_score = self._clamp_score(cred_antispoof_score + cred_score_offset)
        calibrated_cred_score = max(calibrated_cred_score, cred_score_floor)
        calibrated_cred_score = min(calibrated_cred_score, cred_score_ceiling)

        return CalibratedAntispoofSignal(
            final_score=self._clamp_score(calibrated_final_score),
            cred_antispoof_score=self._clamp_score(calibrated_cred_score),
        )

    def _as_float(self, value: object) -> float:
        if isinstance(value, bool):
            return 0.0

        if isinstance(value, int | float):
            return float(value)

        return 0.0

    def _clamp_score(self, value: float) -> float:
        return round(min(max(float(value), 0.0), 1.0), 6)
