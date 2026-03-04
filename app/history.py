from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from app.calculation import Calculation


class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        raise NotImplementedError


class LoggingObserver(HistoryObserver):
    def update(self, calculation: Calculation) -> None:
        logging.info(str(calculation))


class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator) -> None:
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        try:
            self.calculator.save_history()
        except Exception as e:
            logging.warning(f"Auto-save failed: {e}")