class CalculatorError(Exception):
    pass


class ValidationError(CalculatorError):
    pass


class OperationError(CalculatorError):
    pass