import pytest
from src.core.domain.enums.expense_category import ExpenseCategory
from src.use_cases.extract_receipt_data_use_case import ExtractReceiptDataUseCase
from src.core.ports.ocr_engine_interface import IOCREngine
from src.core.ports.nlp_engine_interface import INLPEngine

class MockOCREngine(IOCREngine):
    def extract_text(self, image_bytes: bytes) -> str:
        return "Facture Carburant Total 25000 FCFA"

class MockNLPEngine(INLPEngine):
    def analyze_text(self, text: str) -> dict:
        return {
            "supplier_name": "Station Total",
            "amount": 25000.0,
            "currency": "FCFA",
            "category": "CARBURANT",
            "confidence_score": 0.95
        }

class MockNLPFallbackEngine(INLPEngine):
    def analyze_text(self, text: str) -> dict:
        return {
            "supplier_name": "Inconnu",
            "amount": None,
            "currency": "FCFA",
            "category": "UNKNOWN_CAT",
            "confidence_score": 0.40
        }

def test_extract_receipt_success():
    ocr_engine = MockOCREngine()
    nlp_engine = MockNLPEngine()
    use_case = ExtractReceiptDataUseCase(ocr_engine, nlp_engine)
    
    result = use_case.execute(b"fake_image_bytes")
    
    assert result.supplier_name == "Station Total"
    assert result.total_amount == 25000.0
    assert result.category == ExpenseCategory.CARBURANT
    assert result.confidence_score == 0.95

def test_extract_receipt_fallback_category():
    ocr_engine = MockOCREngine()
    nlp_engine = MockNLPFallbackEngine()
    use_case = ExtractReceiptDataUseCase(ocr_engine, nlp_engine)
    
    result = use_case.execute(b"fake_image_bytes")
    
    # UNKNOWN_CAT should fallback to AUTRE
    assert result.category == ExpenseCategory.AUTRE
    assert result.confidence_score == 0.40
    assert result.total_amount is None
