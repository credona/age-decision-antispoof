import numpy as np

from antispoof.heuristics import BlurHeuristicAnalyzer, BlurHeuristicResult


def test_blur_heuristic_returns_expected_structure():
    analyzer = BlurHeuristicAnalyzer()

    image = np.zeros((80, 80, 3), dtype=np.uint8)
    result = analyzer.analyze(image)

    assert isinstance(result, BlurHeuristicResult)
    assert isinstance(result.score, float)
    assert isinstance(result.threshold, float)
    assert result.label in ["sharp", "blurry"]


def test_blur_heuristic_rejects_invalid_threshold():
    try:
        BlurHeuristicAnalyzer(threshold=-1)
    except ValueError as exc:
        assert str(exc) == "Threshold must be non-negative."
    else:
        raise AssertionError("Expected ValueError for invalid threshold.")