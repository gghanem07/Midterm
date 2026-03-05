from decimal import Decimal
import pytest

from app.calculation import Calculation
from app.exceptions import OperationError


def test_calculation_addition():
    c = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert c.result == Decimal("5")


def test_calculation_unknown_operation():
    with pytest.raises(OperationError):
        Calculation("Nope", Decimal("1"), Decimal("1"))