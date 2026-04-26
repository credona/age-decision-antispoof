from antispoof.models.loader import AntiSpoofModelLoader


def test_model_loader_loads_session():
    session = AntiSpoofModelLoader().load()

    assert session is not None
    assert len(session.get_inputs()) > 0
    assert len(session.get_outputs()) > 0
