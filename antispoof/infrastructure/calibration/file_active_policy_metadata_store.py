import json
from pathlib import Path


class FileActivePolicyMetadataStore:
    def __init__(self, path: str | Path | None) -> None:
        self.path = Path(path) if path else None

    def load_active_policy(self):
        if self.path is None or not self.path.exists():
            return None

        payload = json.loads(self.path.read_text(encoding="utf-8"))

        class ActivePolicyMetadata:
            def __init__(self, benchmark_attestation_id: str | None) -> None:
                self.metadata = type(
                    "Metadata",
                    (),
                    {"benchmark_attestation_id": benchmark_attestation_id},
                )()

        return ActivePolicyMetadata(payload.get("benchmark_attestation_id"))

    def save_from_policy(self, policy) -> None:
        if self.path is None:
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(
                {
                    "policy_id": policy.metadata.policy_id,
                    "benchmark_attestation_id": policy.metadata.benchmark_attestation_id,
                },
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
