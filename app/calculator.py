from __future__ import annotations

import logging
import os
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation

Number = Union[int, float, Decimal]
Result = Union[Number, str]


class Calculator:
    def __init__(self, config: Optional[CalculatorConfig] = None) -> None:
        if config is None:
            project_root = Path(__file__).parent.parent
            config = CalculatorConfig(base_dir=project_root)

        self.config = config
        self.config.validate()

        os.makedirs(self.config.log_dir, exist_ok=True)
        self._setup_logging()

        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None

        self.observers: List[HistoryObserver] = []
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        self._setup_directories()

        try:
            self.load_history()
        except Exception as e:
            logging.warning(f"Could not load history: {e}")

    def _setup_logging(self) -> None:
        log_file = self.config.log_file.resolve()
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            force=True,
        )

    def _setup_directories(self) -> None:
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

    def add_observer(self, observer: HistoryObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: HistoryObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, calculation: Calculation) -> None:
        for observer in self.observers:
            observer.update(calculation)

    def set_operation(self, operation: Operation) -> None:
        self.operation_strategy = operation

    def perform_operation(self, a: Union[str, Number], b: Union[str, Number]) -> Result:
        if not self.operation_strategy:
            raise OperationError("No operation set")

        try:
            da = InputValidator.validate_number(a, self.config)
            db = InputValidator.validate_number(b, self.config)

            result = self.operation_strategy.execute(da, db)

            calc = Calculation(
                operation=str(self.operation_strategy),
                operand1=da,
                operand2=db,
            )

            self.undo_stack.append(CalculatorMemento(self.history.copy()))
            self.redo_stack.clear()

            self.history.append(calc)
            if len(self.history) > self.config.max_history_size:
                self.history.pop(0)

            self.notify_observers(calc)
            return result

        except ValidationError:
            raise
        except Exception as e:
            raise OperationError(f"Operation failed: {e}")

    def save_history(self) -> None:
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

        rows = [
            {
                "operation": c.operation,
                "operand1": str(c.operand1),
                "operand2": str(c.operand2),
                "result": str(c.result),
                "timestamp": c.timestamp.isoformat(),
            }
            for c in self.history
        ]

        df = pd.DataFrame(rows, columns=["operation", "operand1", "operand2", "result", "timestamp"])
        df.to_csv(self.config.history_file, index=False)

    def load_history(self) -> None:
        if not self.config.history_file.exists():
            return

        df = pd.read_csv(self.config.history_file)
        if df.empty:
            self.history = []
            return

        self.history = [
            Calculation.from_dict(
                {
                    "operation": row["operation"],
                    "operand1": row["operand1"],
                    "operand2": row["operand2"],
                    "result": row["result"],
                    "timestamp": row["timestamp"],
                }
            )
            for _, row in df.iterrows()
        ]

    def show_history(self) -> List[str]:
        return [str(c) for c in self.history]

    def clear_history(self) -> None:
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        m = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = m.history.copy()
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        m = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = m.history.copy()
        return True