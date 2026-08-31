from pathlib import Path

from gates_loader import load

schema_match = load("schema_match")

CLI = """
from __future__ import annotations
import argparse, json
SCHEMA = {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"], "additionalProperties": False}
def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--schema", action="store_true")
    p.parse_args(argv)
    print(json.dumps(SCHEMA, separators=(",", ":")))
    return 0
"""

SPEC = """# spec 001

Gate: pass

## Goal

## Interface

```json
{"type":"object","properties":{"id":{"type":"string"}},"required":["id"],"additionalProperties":false}
```

## Tests

## Out of scope
"""


def _pkg(root: Path, schema_extra: str = "") -> None:
    pkg = root / "src" / "demo_pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "entrypoints").mkdir()
    (pkg / "entrypoints" / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "entrypoints" / "cli.py").write_text(CLI, encoding="utf-8")
    spec = root / "specs" / "001"
    spec.mkdir(parents=True)
    text = SPEC
    if schema_extra:
        text = text.replace('"id":{"type":"string"}', schema_extra)
    (spec / "spec.md").write_text(text, encoding="utf-8")
    (root / "specs" / ".active").write_text("001\n", encoding="utf-8")


def test_schema_matches(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path)
    monkeypatch.setattr(
        schema_match.sys,
        "argv",
        ["schema_match", "--root", str(tmp_path), "--spec", "001"],
    )
    assert schema_match.main() == 0


def test_schema_mismatch(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path, '"id":{"type":"integer"}')
    monkeypatch.setattr(
        schema_match.sys,
        "argv",
        ["schema_match", "--root", str(tmp_path), "--spec", "001"],
    )
    assert schema_match.main() == 1
