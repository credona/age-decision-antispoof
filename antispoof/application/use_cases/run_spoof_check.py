from antispoof.application.dto.check_command import CheckCommand
from antispoof.application.ports.pipeline import SpoofCheckPipelinePort


class RunSpoofCheckUseCase:
    """
    Application use case for spoof check execution.

    The API layer owns request parsing and public response filtering.
    The pipeline owns spoof check inference and fusion.
    """

    def __init__(self, pipeline: SpoofCheckPipelinePort):
        self.pipeline = pipeline

    def execute(self, command: CheckCommand):
        return self.pipeline.predict_from_bytes(command.image_bytes)
