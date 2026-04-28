import numpy as np

from antispoof.heuristics import TextureHeuristicAnalyzer, TextureHeuristicResult


def test_texture_heuristic_returns_expected_structure():
    analyzer = TextureHeuristicAnalyzer()

    image = np.zeros((80, 80, 3), dtype=np.uint8)
    result = analyzer.analyze(image)

    assert isinstance(result, TextureHeuristicResult)
    assert isinstance(result.score, float)
    assert isinstance(result.threshold, float)
    assert result.label in ["real", "spoof"]


def test_texture_heuristic_rejects_invalid_threshold():
    try:
        TextureHeuristicAnalyzer(threshold=-1)
    except ValueError as exc:
        assert str(exc) == "Threshold must be non-negative."
    else:
        raise AssertionError("Expected ValueError for invalid threshold.")
