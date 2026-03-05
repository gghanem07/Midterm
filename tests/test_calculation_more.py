import pytest
import datetime
from decimal import Decimal

from app.calculation import Calculation
from app.exceptions import OperationError


def test_calculation_divide_by_zero():
    with pytest.raises(OperationError):
        Calculation("Division", Decimal("5"), Decimal("0"))


def test_calculation_negative_power():
    with pytest.raises(OperationError):
        Calculation("Power", Decimal("2"), Decimal("-1"))


def test_calculation_invalid_root_degree_zero():
    with pytest.raises(OperationError):
        Calculation("Root", Decimal("9"), Decimal("0"))


def test_calculation_invalid_root_negative_number():
    with pytest.raises(OperationError):
        Calculation("Root", Decimal("-9"), Decimal("2"))


def test_calculation_from_dict_success():
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.datetime.now().isoformat(),
    }

    calc = Calculation.from_dict(data)

    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_calculation_from_dict_invalid_data():
    bad_data = {
        "operation": "Addition",
        "operand1": "not_a_number",
        "operand2": "3",
        "result": "5",
        "timestamp": "bad_timestamp",
    }

    with pytest.raises(OperationError):
        Calculation.from_dict(bad_data)


def test_calculation_to_dict_str_and_repr():
    calc = Calculation("Addition", Decimal("1"), Decimal("2"))

    d = calc.to_dict()
    assert d["operation"] == "Addition"
    assert d["operand1"] == "1"
    assert d["operand2"] == "2"
    assert d["result"] == "3"
    assert "timestamp" in d

    assert str(calc) == "Addition(1, 2) = 3"
    assert "Calculation(" in repr(calc)


def test_calculation_eq_non_calculation_returns_notimplemented():
    calc = Calculation("Addition", Decimal("1"), Decimal("2"))
    assert calc.__eq__(123) is NotImplemented
    assert (calc == 123) is False


def test_calculation_format_result():
    calc = Calculation("Division", Decimal("1"), Decimal("2"))
    assert calc.format_result(precision=2) == "0.5"

def test_calculation_subtraction_path():
    c = Calculation("Subtraction", Decimal("5"), Decimal("2"))
    assert c.result == Decimal("3")


def test_calculation_eq_notimplemented_line():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    assert c.__eq__("x") is NotImplemented