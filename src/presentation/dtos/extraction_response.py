from pydantic import BaseModel
from typing import Optional
from src.core.domain.enums.expense_category import ExpenseCategory

class ExtractionResponseDTO(BaseModel):
    supplier_name: Optional[str]
    total_amount: Optional[float]
    currency: str
    category: ExpenseCategory
    confidence_score: float
