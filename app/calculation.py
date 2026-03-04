from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Any, Dict

from app.exceptions import OperationError


@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal = field(init=False)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        self.result = self.calculate()

    def calculate(self) -> Decimal:
        ops = {
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": lambda x, y: x / y if y != 0 else self._div_zero(),
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._neg_exp(),
            "Root": lambda x, y: Decimal(pow(float(x), 1 / float(y))) if x >= 0 and y != 0 else self._bad_root(x, y),
        }

        fn = ops.get(self.operation)
        if not fn:
            raise OperationError(f"Unknown operation: {self.operation}")

        try:
            return fn(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            raise OperationError(f"Calculation failed: {e}")

    @staticmethod
    def _div_zero() -> Decimal:
        raise OperationError("Division by zero is not allowed")

    @staticmethod
    def _neg_exp() -> Decimal:
        raise OperationError("Negative exponents are not supported")

    @staticmethod
    def _bad_root(x: Decimal, y: Decimal) -> Decimal:
        if y == 0:
            raise OperationError("Zero root is undefined")
        if x < 0:
            raise OperationError("Cannot calculate root of negative number")
        raise OperationError("Invalid root operation")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Calculation":
        calc = Calculation(
            operation=data["operation"],
            operand1=Decimal(data["operand1"]),
            operand2=Decimal(data["operand2"]),
        )
        calc.timestamp = datetime.fromisoformat(data["timestamp"])
        return calc

    def __str__(self) -> str:
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"