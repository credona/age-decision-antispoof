from antispoof.privacy import build_privacy_metadata


def test_build_privacy_metadata():
    """Test privacy metadata contract."""
    metadata = build_privacy_metadata()

    assert metadata["privacy_first"] is True
    assert metadata["image_persisted"] is False
    assert metadata["biometric_template_stored"] is False
    assert metadata["raw_image_logged"] is False
    assert metadata["processing_scope"] == "in_memory_inference_only"
    assert metadata["retention_policy"] == "no_image_retention"
