from pathlib import Path

from gates_loader import load

spec_exists = load("spec_exists")


def test_src_without_spec(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x=1\n", encoding="utf-8")
    monkeypatch.setattr(spec_exists.sys, "argv", ["spec_exists", "--root", str(tmp_path)])
    assert spec_exists.main() == 1


def test_src_with_spec(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "src").mkdir()
    spec = tmp_path / "specs" / "001"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text("Gate: pass\n", encoding="utf-8")
    monkeypatch.setattr(
        spec_exists.sys,
        "argv",
        ["spec_exists", "--root", str(tmp_path), "--spec", "001"],
    )
    assert spec_exists.main() == 0
