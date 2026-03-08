import pytest
from decimal import Decimal

from app.input_validators import InputValidator
from app.exceptions import ValidationError


def test_validate_number_accepts_string_int_float_decimal():
    assert InputValidator.validate_number("10") == Decimal("10")
    assert InputValidator.validate_number(10) == Decimal("10")
    assert InputValidator.validate_number(10.5) == Decimal("10.5")
    assert InputValidator.validate_number(Decimal("2.25")) == Decimal("2.25")


def test_validate_number_strips_spaces_and_commas():
    assert InputValidator.validate_number("  1,234.50 ") == Decimal("1234.50")


def test_validate_number_rejects_empty_string():
    with pytest.raises(ValidationError):
        InputValidator.validate_number("")


def test_validate_number_rejects_non_numeric_string():
    with pytest.raises(ValidationError):
        InputValidator.validate_number("abc")


def test_validate_number_rejects_unsupported_type():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(["10"])


class DummyConfig:
    decimal_precision = 2


def test_validate_number_rejects_too_many_decimal_places():
    with pytest.raises(ValidationError):
        InputValidator.validate_number("1.234", DummyConfig())


def test_validate_number_rejects_object_type():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(object())