########################
# Operation Classes    #
########################

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Type

from app.exceptions import ValidationError


class Operation(ABC):
    """Base interface for all operations (Strategy)."""

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError  # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Optional validation hook for subclasses."""
        return

    def __str__(self) -> str:
        return self.__class__.__name__


class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a + b


class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a - b


class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a * b


class Division(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a / b


class Power(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        # Decimal ** Decimal is tricky for non-integers; use float fallback for now
        return Decimal(pow(float(a), float(b)))


class Root(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))


class OperationFactory:
    """Factory Pattern: create Operation objects by a string key."""

    _operations: Dict[str, Type[Operation]] = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: Type[Operation]) -> None:
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        op_class = cls._operations.get(operation_type.lower())
        if not op_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return op_class()