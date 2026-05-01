from dataclasses import dataclass
from typing import Optional
from src.core.domain.enums.expense_category import ExpenseCategory

@dataclass
class ReceiptExtraction:
    supplier_name: Optional[str]
    total_amount: Optional[float]
    currency: str
    category: ExpenseCategory
    confidence_score: float
