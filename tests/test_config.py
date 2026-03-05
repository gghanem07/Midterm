from pathlib import Path
from app.calculator_config import CalculatorConfig


def test_config_dirs(tmp_path: Path):
    cfg = CalculatorConfig(base_dir=tmp_path)
    assert cfg.base_dir == tmp_path
    assert cfg.data_dir.exists()
    assert cfg.logs_dir.exists()