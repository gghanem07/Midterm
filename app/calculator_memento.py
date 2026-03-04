from dataclasses import dataclass
from typing import List

from app.calculation import Calculation


@dataclass(frozen=True)
class CalculatorMemento:
    history: List[Calculation]