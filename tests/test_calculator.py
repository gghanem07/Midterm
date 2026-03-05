from app.calculator import Calculator
from app.operations import OperationFactory


def test_calculator_perform_operation_add():
    c = Calculator()
    c.set_operation(OperationFactory.create_operation("add"))
    assert str(c.perform_operation("2", "3")) in {"5", "5.0"}


def test_calculator_undo_redo_flow():
    c = Calculator()
    c.set_operation(OperationFactory.create_operation("add"))
    c.perform_operation("2", "3")
    assert c.undo() is True
    assert c.redo() is True