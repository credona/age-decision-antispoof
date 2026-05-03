from benchmarks.common.report import assert_report_is_privacy_safe, build_benchmark_report


def test_benchmark_report_is_privacy_safe():
    report = build_benchmark_report(
        benchmark_target="model",
        durations_ms=[10.0, 12.0, 14.0],
        labels=["real", "spoof", "real"],
        error_rates={
            "apcer": 0.0,
            "bpcer": 0.0,
            "acer": 0.0,
            "attack_count": 1,
            "bona_fide_count": 2,
        },
        command="python -m benchmarks.model.run_model_benchmark",
        sample_count=3,
    )

    assert_report_is_privacy_safe(report)

    serialized = str(report).lower()

    assert "estimated_age" not in serialized
    assert "confidence" not in serialized
    assert "raw_scores" not in serialized
    assert "'threshold':" not in serialized
    assert "model_path" not in serialized
    assert "base64" not in serialized
    assert "payload" not in serialized
    assert "downstream_response" not in serialized
    assert "labels_csv" not in serialized


def test_benchmark_report_rejects_forbidden_fields():
    report = build_benchmark_report(
        benchmark_target="model",
        durations_ms=[10.0],
        labels=["real"],
        error_rates={
            "apcer": 0.0,
            "bpcer": 0.0,
            "acer": 0.0,
            "attack_count": 0,
            "bona_fide_count": 1,
        },
        command="python -m benchmarks.model.run_model_benchmark",
        sample_count=1,
    )

    report["threshold"] = 0.5

    try:
        assert_report_is_privacy_safe(report)
    except ValueError as exc:
        assert "Forbidden benchmark report field detected" in str(exc)
    else:
        raise AssertionError("Expected forbidden field to be rejected")
