from antispoof.application.dto.check_command import CheckCommand
from antispoof.application.ports.pipeline import AntiSpoofPipelinePort


class CheckLivenessUseCase:
    """
    Application use case for anti-spoofing checks.

    The API layer owns request parsing and public response filtering.
    The pipeline owns PAD inference and fusion.
    """

    def __init__(self, pipeline: AntiSpoofPipelinePort):
        self.pipeline = pipeline

    def execute(self, command: CheckCommand):
        return self.pipeline.predict_from_bytes(command.image_bytes)
