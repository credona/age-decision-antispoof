from abc import ABC, abstractmethod


class SpoofCheckPipelinePort(ABC):
    @abstractmethod
    def predict_from_bytes(self, image_bytes: bytes):
        pass
