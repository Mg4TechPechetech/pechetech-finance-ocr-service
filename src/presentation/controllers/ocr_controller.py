import asyncio
from functools import lru_cache
from fastapi import APIRouter, UploadFile, File, Depends
from src.use_cases.extract_receipt_data_use_case import ExtractReceiptDataUseCase
from src.infrastructure.engines.tesseract_ocr_engine import TesseractOCREngine
from src.infrastructure.engines.simple_nlp_engine import SimpleNLPEngine
from src.presentation.dtos.extraction_response import ExtractionResponseDTO

router = APIRouter(tags=["OCR"])

# Dependency Injection
@lru_cache()  # Cache DI to avoid instantiating ML models per request
def get_extract_use_case():
    ocr_engine = TesseractOCREngine()
    nlp_engine = SimpleNLPEngine()
    return ExtractReceiptDataUseCase(ocr_engine, nlp_engine)

@router.post("/extract", response_model=ExtractionResponseDTO)
async def extract_receipt(
    file: UploadFile = File(...),
    use_case: ExtractReceiptDataUseCase = Depends(get_extract_use_case)
):
    image_bytes = await file.read()
    
    # Execute Use Case offloaded to thread to avoid blocking event loop
    result = await asyncio.to_thread(use_case.execute, image_bytes)
    
    # Map to DTO
    return ExtractionResponseDTO(
        supplier_name=result.supplier_name,
        total_amount=result.total_amount,
        currency=result.currency,
        category=result.category,
        confidence_score=result.confidence_score
    )
