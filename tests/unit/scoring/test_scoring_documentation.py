from pathlib import Path


def test_scoring_documentation_defines_cred_antispoof_score_formula():
    content = Path("docs/scoring.md").read_text(encoding="utf-8")

    assert "cred_antispoof_score" in content
    assert "raw_final_score" in content
    assert "calibrated_score = clamp" in content
    assert "credona.antispoof.fusion-threshold.v1" in content


def test_scoring_documentation_preserves_privacy_contract():
    content = Path("docs/scoring.md").read_text(encoding="utf-8")

    assert "raw model scores" in content
    assert "raw logits" in content
    assert "internal threshold" in content
