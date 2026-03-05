from decimal import Decimal
import pytest

from app.operations import OperationFactory
from app.exceptions import ValidationError


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("add", "2", "3", Decimal("5")),
        ("subtract", "5", "2", Decimal("3")),
        ("multiply", "2", "4", Decimal("8")),
        ("divide", "8", "2", Decimal("4")),
        ("power", "2", "3", Decimal("8")),
        ("root", "9", "2", Decimal("3")),
        ("modulus", "10", "3", Decimal("1")),
        ("intdiv", "10", "3", Decimal("3")),
        ("percentage", "50", "200", Decimal("100")),
        ("absdiff", "5", "12", Decimal("7")),
    ],
)
def test_operations_execute(op, a, b, expected):
    operation = OperationFactory.create_operation(op)
    result = operation.execute(Decimal(a), Decimal(b))
    assert result == expected


def test_divide_by_zero_raises():
    operation = OperationFactory.create_operation("divide")
    with pytest.raises(ValidationError):
        operation.execute(Decimal("1"), Decimal("0"))