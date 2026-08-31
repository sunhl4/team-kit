from pathlib import Path

from gates_loader import load

spec_headings = load("spec_headings")


def test_missing_heading(tmp_path: Path) -> None:
    path = tmp_path / "spec.md"
    path.write_text("# spec\n\nGate: pending\n\n## Goal\n\n## Interface\n\n## Tests\n", encoding="utf-8")
    errors = spec_headings.check_spec(path)
    assert any("Out of scope" in e for e in errors)


def test_ok(tmp_path: Path) -> None:
    path = tmp_path / "spec.md"
    path.write_text(
        "# spec\n\nGate: pass\n\n## Goal\n\n## Interface\n\n## Tests\n\n## Out of scope\n",
        encoding="utf-8",
    )
    assert spec_headings.check_spec(path) == []


def test_invalid_gate(tmp_path: Path) -> None:
    path = tmp_path / "spec.md"
    path.write_text(
        "# spec\n\nGate: maybe\n\n## Goal\n\n## Interface\n\n## Tests\n\n## Out of scope\n",
        encoding="utf-8",
    )
    errors = spec_headings.check_spec(path)
    assert any("Gate" in e for e in errors)
