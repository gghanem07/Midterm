import builtins
import pytest

from app import repl


def test_repl_help_then_exit(monkeypatch, capsys):
    inputs = iter(["help", "exit"])

    def fake_input(_prompt=""):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "started" in out
    assert "commands" in out
    assert "goodbye" in out