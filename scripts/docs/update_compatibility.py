import json
from pathlib import Path

PROJECT_FILE = Path("project.json")
COMPATIBILITY_FILE = Path("compatibility.json")


def main() -> None:
    project = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))

    major_version = project["version"].split(".")[0]

    compatibility = {
        "service": project["service_name"],
        "version": project["version"],
        "contract_version": project["contract_version"],
        "compatible_with": {
            "age-decision-api": f">={major_version}.0.0 <{int(major_version) + 1}.0.0",
            "age-decision-js": f">={major_version}.0.0 <{int(major_version) + 1}.0.0",
        },
        "public_contract": {
            "decision_values": ["real", "spoof"],
            "score_field": "cred_antispoof_score",
            "raw_model_scores_exposed": False,
            "heuristic_details_exposed": False,
            "calibration_details_exposed": False,
            "legacy_cred_score_exposed": False,
        },
    }

    COMPATIBILITY_FILE.write_text(
        json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
