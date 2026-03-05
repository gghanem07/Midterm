import builtins
from pathlib import Path

from app.repl import calculator_repl


def run_repl(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _="": next(it))


def test_repl_add_happy_path(monkeypatch, capsys, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    run_repl(monkeypatch, ["add", "2", "3", "exit"])
    calculator_repl()
    out = capsys.readouterr().out
    assert "Result:" in out


def test_repl_clear_then_history(monkeypatch, capsys, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    run_repl(monkeypatch, ["clear", "history", "exit"])
    calculator_repl()
    out = capsys.readouterr().out
    assert "History cleared" in out
    assert "No history" in out


def test_repl_undo_redo_empty(monkeypatch, capsys, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    run_repl(monkeypatch, ["undo", "redo", "exit"])
    calculator_repl()
    out = capsys.readouterr().out
    assert "Nothing to undo" in out
    assert "Nothing to redo" in out


def test_repl_unknown_command(monkeypatch, capsys, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    run_repl(monkeypatch, ["not_a_command", "exit"])
    calculator_repl()
    out = capsys.readouterr().out
    assert "Unknown command. Type 'help' to see available commands." in out
    assert "Goodbye" in out