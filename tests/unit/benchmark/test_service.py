import pytest

from antispoof.benchmark import run_local_benchmark


def test_run_local_benchmark_rejects_missing_dataset(tmp_path):
    """Test local benchmark rejects missing labels.csv."""
    with pytest.raises(FileNotFoundError):
        run_local_benchmark(dataset_dir=tmp_path)