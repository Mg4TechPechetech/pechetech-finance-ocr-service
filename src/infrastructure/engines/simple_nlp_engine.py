import re
from src.core.ports.nlp_engine_interface import INLPEngine

class SimpleNLPEngine(INLPEngine):
    def analyze_text(self, text: str) -> dict:
        text_lower = text.lower()
        
        # 1. Extract Amount
        amount = self._extract_amount(text)
        
        # 2. Extract Category
        category = self._classify_category(text_lower)
        
        # 3. Extract Supplier (First line usually)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        supplier = lines[0] if lines else "Inconnu"
        
        return {
            "amount": amount,
            "category": category,
            "supplier_name": supplier,
            "currency": "FCFA",
            "confidence_score": 0.92
        }

    def _extract_amount(self, text: str) -> float:
        cfa_pattern = r'(\d+)\s?(?:CFA|FCFA|F)'
        amounts = re.findall(cfa_pattern, text, re.IGNORECASE)
        
        if not amounts:
            # Fallback to generic number pattern
            amount_pattern = r'(\d{1,3}(?:\s?\d{3})*(?:[.,]\d{2})?)'
            amounts = re.findall(amount_pattern, text)

        clean_amounts = []
        for a in amounts:
            try:
                # Remove spaces and normalize decimal separator
                clean_val = float(a.replace('\s', '').replace(' ', '').replace(',', '.'))
                clean_amounts.append(clean_val)
            except ValueError:
                continue
        
        return max(clean_amounts) if clean_amounts else 0.0

    def _classify_category(self, text: str) -> str:
        categories = {
            "CARBURANT": ["essence", "gasoil", "carburant", "total", "shell", "station"],
            "GLACE": ["glace", "galace", "froid", "bloc"],
            "APPATS": ["appat", "yaboy", "appâts"],
            "VIVRES": ["riz", "huile", "sucre", "pain", "vivres", "boutique"],
            "ENTRETIEN": ["moteur", "reparation", "piece", "entretien", "filet"]
        }
        
        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return cat
        
        return "AUTRE"
