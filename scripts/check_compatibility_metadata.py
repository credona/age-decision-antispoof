import json
from pathlib import Path

PROJECT_FILE = Path("project.json")
COMPATIBILITY_FILE = Path("compatibility.json")

EXPECTED_DECISION_VALUES = ["real", "spoof"]
EXPECTED_SCORE_FIELD = "cred_antispoof_score"


def main() -> None:
    project = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
    compatibility = json.loads(COMPATIBILITY_FILE.read_text(encoding="utf-8"))

    assert_equal("service", compatibility["service"], project["service_name"])
    assert_equal("version", compatibility["version"], project["version"])
    assert_equal(
        "contract_version",
        compatibility["contract_version"],
        project["contract_version"],
    )

    public_contract = compatibility["public_contract"]

    assert_equal(
        "decision_values",
        public_contract["decision_values"],
        EXPECTED_DECISION_VALUES,
    )
    assert_equal("score_field", public_contract["score_field"], EXPECTED_SCORE_FIELD)
    assert_false("raw_model_scores_exposed", public_contract["raw_model_scores_exposed"])
    assert_false("heuristic_details_exposed", public_contract["heuristic_details_exposed"])
    assert_false(
        "calibration_details_exposed",
        public_contract["calibration_details_exposed"],
    )
    assert_false("legacy_cred_score_exposed", public_contract["legacy_cred_score_exposed"])

    compatible_with = compatibility["compatible_with"]

    for repository, version_range in compatible_with.items():
        if not repository.startswith("age-decision-"):
            raise SystemExit(f"Invalid repository name in compatibility matrix: {repository}")

        if not version_range.startswith(">=") or "<" not in version_range:
            raise SystemExit(f"Invalid compatibility range for {repository}: {version_range}")


def assert_equal(name: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise SystemExit(f"{name} mismatch: expected {expected}, got {actual}")


def assert_false(name: str, value: bool) -> None:
    if value is not False:
        raise SystemExit(f"{name} must be false")


if __name__ == "__main__":
    main()
