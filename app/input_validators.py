########################
# Input Validators     #
########################

from decimal import Decimal, InvalidOperation
from typing import Union

from app.exceptions import ValidationError

NumberLike = Union[str, int, float, Decimal]


class InputValidator:
    """
    Validates and converts user input into Decimal.

    """

    @staticmethod
    def validate_number(value: NumberLike, config=None) -> Decimal:
        """
        Convert a value to Decimal with validation.

        - Accepts str/int/float/Decimal
        - Rejects empty strings and non-numeric input
        - Optionally enforces precision if config is provided
        """
        # 1) Handle strings
        if isinstance(value, str):
            cleaned = value.strip()
            if cleaned == "":
                raise ValidationError("Input cannot be empty")

            # Allow commas like 
            cleaned = cleaned.replace(",", "")

            try:
                dec = Decimal(cleaned)
            except InvalidOperation:
                raise ValidationError(f"Invalid number: '{value}'")

        # 2) Handle Decimal already
        elif isinstance(value, Decimal):
            dec = value

        # 3) Handle int/float
        elif isinstance(value, (int, float)):
            # Convert through str to reduce float representation surprises
            try:
                dec = Decimal(str(value))
            except InvalidOperation:
                raise ValidationError(f"Invalid number: '{value}'")

        else:
            raise ValidationError(f"Unsupported input type: {type(value).__name__}")

        # Optional: enforce decimal precision if your config supports it
        if config is not None:
            precision = getattr(config, "decimal_precision", None)
            if isinstance(precision, int) and precision >= 0:
                # If number has too many decimal places, reject it
                exponent = -dec.as_tuple().exponent  # digits after decimal
                if exponent > precision:
                    raise ValidationError(
                        f"Too many decimal places (max {precision})"
                    )

        return dec