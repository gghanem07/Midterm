from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class CalculatorConfig:
    base_dir: Path
    max_history_size: int = 100
    decimal_precision: int = 10

    @property
    def data_dir(self) -> Path:
        return self.base_dir / "data"

    @property
    def history_dir(self) -> Path:
        return self.data_dir

    @property
    def history_file(self) -> Path:
        return self.history_dir / "history.csv"

    @property
    def log_dir(self) -> Path:
        return self.base_dir / "logs"

    @property
    def log_file(self) -> Path:
        return self.log_dir / "app.log"

    def validate(self) -> None:
        if self.max_history_size <= 0:
            raise ValueError("max_history_size must be > 0")

        if self.decimal_precision <= 0:
            raise ValueError("decimal_precision must be > 0")

        os.makedirs(self.history_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)