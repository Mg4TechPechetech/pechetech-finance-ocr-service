from fastapi import FastAPI
from src.presentation.controllers.ocr_controller import router as ocr_router

app = FastAPI(
    title="PecheTech Finance OCR Service",
    description="Micro-service IA for receipt OCR and NLP classification",
    version="1.0.0"
)

app.include_router(ocr_router)

@app.get("/health")
def health_check():
    return {"status": "up"}
