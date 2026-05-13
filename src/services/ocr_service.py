import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import re

class OCRService:
    def __init__(self):
        # Tesseract configuration for better results on receipts
        self.tess_config = '--psm 6'

    def preprocess_image(self, image_bytes):
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 1. Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Adaptive Binarization (handles shadows/bad lighting)
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # 3. Denoising
        denoised = cv2.fastNlMeansDenoising(binary, h=10)

        return denoised

    def extract_text(self, image_bytes):
        # Preprocess
        processed_img = self.preprocess_image(image_bytes)
        
        # Convert back to PIL for Tesseract
        pil_img = Image.fromarray(processed_img)
        
        # OCR
        text = pytesseract.image_to_string(pil_img, config=self.tess_config, lang='fra+eng')
        return text

    def parse_receipt(self, text):
        # Basic regex patterns for Amount and Date
        # Match "10000" or "10 000" or "10,000.00"
        amount_pattern = r'(\d{1,3}(?:\s?\d{3})*(?:[.,]\d{2})?)'
        # Look for typical Senegalese context (CFA, FCFA)
        cfa_pattern = r'(\d+)\s?(?:CFA|FCFA|F)'
        
        amounts = re.findall(cfa_pattern, text, re.IGNORECASE)
        if not amounts:
            amounts = re.findall(amount_pattern, text)

        # Filter and get the highest amount (usually the total)
        clean_amounts = []
        for a in amounts:
            try:
                clean_val = float(a.replace(' ', '').replace(',', '.'))
                clean_amounts.append(clean_val)
            except ValueError:
                continue
        
        total_amount = max(clean_amounts) if clean_amounts else 0.0
        
        # Categorization logic
        category = self._classify_category(text)
        
        return {
            "total_amount": total_amount,
            "category": category,
            "raw_text": text
        }

    def _classify_category(self, text):
        text = text.lower()
        
        categories = {
            "CARBURANT": ["essence", "gasoil", "carburant", "station", "total", "shell", "ola"],
            "GLACE": ["glace", "galace", "froid", "bloc"],
            "APPATS": ["appat", "appâts", "yaboy", "appats"],
            "VIVRES": ["riz", "huile", "sucre", "pain", "vivres", "alimentation", "boutique"],
            "ENTRETIEN": ["moteur", "reparation", "piece", "entretien", "filet", "corde"]
        }
        
        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return cat
        
        return "AUTRE"
