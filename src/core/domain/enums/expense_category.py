from enum import Enum

class ExpenseCategory(str, Enum):
    CARBURANT = "CARBURANT"
    GLACE = "GLACE"
    APPATS = "APPATS"
    VIVRES = "VIVRES"
    ENTRETIEN = "ENTRETIEN"
    AUTRE = "AUTRE"
