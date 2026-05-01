from abc import ABC, abstractmethod
from typing import Dict, Any

class INLPEngine(ABC):
    @abstractmethod
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Returns structured data: supplier, amount, category, etc."""
        pass
