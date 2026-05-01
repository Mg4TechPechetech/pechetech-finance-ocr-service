from src.core.ports.nlp_engine_interface import INLPEngine
from typing import Dict, Any

class DummyNLPEngine(INLPEngine):
    def analyze_text(self, text: str) -> Dict[str, Any]:
        # Mocking Transformer NLP analysis
        # In a real scenario, this would use a CamemBERT or custom model
        
        if "Glace" in text or "glace" in text:
            category = "GLACE"
        elif "appat" in text.lower():
            category = "APPATS"
        elif "carburant" in text.lower() or "essence" in text.lower():
            category = "CARBURANT"
        else:
            category = "AUTRE"

        return {
            "supplier_name": "Aliou Glace",
            "amount": 15000.0,
            "currency": "FCFA",
            "category": category,
            "confidence_score": 0.92
        }
