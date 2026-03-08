from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class CalculatorConfig:
    base_dir: Path
    max_history_size: int = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
    decimal_precision: int = int(os.getenv("CALCULATOR_PRECISION", "10"))

    @property
    def data_dir(self) -> Path:
        p = self.base_dir / "data"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def logs_dir(self) -> Path:
        p = self.base_dir / "logs"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def log_dir(self) -> Path:
        return self.logs_dir

    @property
    def log_file(self) -> Path:
        return self.logs_dir / "calculator.log"

    @property
    def history_dir(self) -> Path:
        p = self.data_dir / "history"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def history_file(self) -> Path:
        return self.history_dir / "history.csv"

    def validate(self) -> None:
        _ = self.data_dir
        _ = self.logs_dir
        _ = self.log_file
        _ = self.history_dir
        _ = self.history_file