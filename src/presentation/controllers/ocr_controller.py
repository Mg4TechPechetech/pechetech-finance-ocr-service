import asyncio
from functools import lru_cache
from fastapi import APIRouter, UploadFile, File, Depends
from starlette.concurrency import run_in_threadpool
from src.use_cases.extract_receipt_data_use_case import ExtractReceiptDataUseCase
from src.infrastructure.engines.dummy_ocr_engine import DummyOCREngine
from src.infrastructure.engines.dummy_nlp_engine import DummyNLPEngine
from src.presentation.dtos.extraction_response import ExtractionResponseDTO

router = APIRouter(prefix="/api/v1/ocr", tags=["OCR"])

# Dependency Injection
@lru_cache()
def get_extract_use_case():
    ocr_engine = DummyOCREngine()
    nlp_engine = DummyNLPEngine()
    return ExtractReceiptDataUseCase(ocr_engine, nlp_engine)

@router.post("/extract", response_model=ExtractionResponseDTO)
async def extract_receipt(
    file: UploadFile = File(...),
    use_case: ExtractReceiptDataUseCase = Depends(get_extract_use_case)
):
    image_bytes = await file.read()
    
    # Execute Use Case (Offloaded to threadpool to avoid blocking event loop)
    # ⚡ Bolt: Offloading synchronous, CPU-intensive ML/OCR operations to a background thread
    result = await run_in_threadpool(use_case.execute, image_bytes)
    
    # Map to DTO
    return ExtractionResponseDTO(
        supplier_name=result.supplier_name,
        total_amount=result.total_amount,
        currency=result.currency,
        category=result.category,
        confidence_score=result.confidence_score
    )
