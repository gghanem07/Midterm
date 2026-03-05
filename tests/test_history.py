from app.history import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.operations import OperationFactory


def test_logging_observer_does_not_crash():
    obs = LoggingObserver()
    obs.update("test")


def test_autosave_observer_calls_save(monkeypatch):
    c = Calculator()
    called = {"n": 0}

    def fake_save():
        called["n"] += 1

    monkeypatch.setattr(c, "save_history", fake_save)

    obs = AutoSaveObserver(c)
    obs.update("anything")
    assert called["n"] == 1


def test_calculator_notifies_observers_on_operation(monkeypatch):
    c = Calculator()
    c.set_operation(OperationFactory.create_operation("add"))

    called = {"n": 0}

    class DummyObserver:
        def update(self, _):
            called["n"] += 1

    c.add_observer(DummyObserver())
    c.perform_operation("2", "3")
    assert called["n"] >= 1