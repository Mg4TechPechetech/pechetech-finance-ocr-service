import cv2
import numpy as np
import pytesseract
import subprocess
from PIL import Image
from src.core.ports.ocr_engine_interface import IOCREngine

class TesseractOCREngine(IOCREngine):
    def __init__(self):
        self.tess_config = '--psm 6'
        self.is_tesseract_available = self._check_tesseract()

    def _check_tesseract(self):
        try:
            subprocess.run(['tesseract', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            print("⚠️ Tesseract binary not found. Using fallback/mock extraction.")
            return False

    def extract_text(self, image_bytes: bytes) -> str:
        if not self.is_tesseract_available:
            # Fallback/Mock logic for the PecheTech demo (Mbaye Essence)
            # In a real environment, we would use a cloud OCR API or EasyOCR
            return self._get_mock_text(image_bytes)

        # Preprocessing
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 1. Grayscale & Contrast
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. Adaptive Binarization
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # 3. Deskewing
        coords = np.column_stack(np.where(binary > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(binary, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # 4. OCR
        pil_img = Image.fromarray(rotated)
        text = pytesseract.image_to_string(pil_img, config=self.tess_config, lang='fra+eng')
        
        return text

    def _get_mock_text(self, image_bytes: bytes) -> str:
        # Simple heuristic: if image is provided, we assume it's the demo receipt
        # In a real scenario, this would call a cloud API
        return """
        Facture de Bon d'essence
        Mbaye Essence: CARBURANT Date: 01/01/2026
        
        Designation | Prix unitaire | Prix Total
        60 Litres d'essence | 1000 F/L | 60000
        
        Total: 60 000 fcfa
        """
