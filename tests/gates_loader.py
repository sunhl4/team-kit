from __future__ import annotations

import importlib.util
from pathlib import Path

GATES = Path(__file__).resolve().parents[1] / "gates"


def load(name: str):
    path = GATES / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
