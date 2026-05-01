from src.core.ports.ocr_engine_interface import IOCREngine
import cv2
import numpy as np

class DummyOCREngine(IOCREngine):
    def extract_text(self, image_bytes: bytes) -> str:
        # Mocking OpenCV Preprocessing
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # In a real scenario:
        # 1. Binarisation adaptative
        # 2. Deskewing
        # 3. Denoising
        # 4. Tesseract/ResNet extraction
        
        # Returning mock extracted text
        return "Glace Thiebou dieune 15000 FCFA"
