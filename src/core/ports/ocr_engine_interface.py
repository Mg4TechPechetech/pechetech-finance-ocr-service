from abc import ABC, abstractmethod

class IOCREngine(ABC):
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> str:
        pass
