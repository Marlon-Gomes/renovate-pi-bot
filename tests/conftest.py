import importlib.util
from pathlib import Path

import pytest


@pytest.fixture()
def mod(monkeypatch):
    path = Path(__file__).resolve().parents[1] / "tools" / "renovate_log_formatter.py"
    spec = importlib.util.spec_from_file_location("renovate_log_formatter.py", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module
