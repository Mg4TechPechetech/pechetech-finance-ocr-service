from src.core.ports.ocr_engine_interface import IOCREngine
from src.core.ports.nlp_engine_interface import INLPEngine
from src.core.domain.entities.receipt_extraction import ReceiptExtraction
from src.core.domain.enums.expense_category import ExpenseCategory

class ExtractReceiptDataUseCase:
    def __init__(self, ocr_engine: IOCREngine, nlp_engine: INLPEngine):
        self.ocr_engine = ocr_engine
        self.nlp_engine = nlp_engine
        
    def execute(self, image_bytes: bytes) -> ReceiptExtraction:
        # 1. OCR Extraction (Pre-processing is handled by the OCR engine implementation)
        raw_text = self.ocr_engine.extract_text(image_bytes)
        
        # 2. NLP Semantic Classification & NER
        structured_data = self.nlp_engine.analyze_text(raw_text)
        
        # 3. Map to Domain Entity
        category_str = structured_data.get('category', 'AUTRE')
        try:
            category = ExpenseCategory(category_str)
        except ValueError:
            category = ExpenseCategory.AUTRE

        return ReceiptExtraction(
            supplier_name=structured_data.get('supplier_name'),
            total_amount=structured_data.get('amount'),
            currency=structured_data.get('currency', 'FCFA'),
            category=category,
            confidence_score=structured_data.get('confidence_score', 0.85)
        )
