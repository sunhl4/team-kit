from pathlib import Path

from gates_loader import load
from gitutil import git_commit, git_init

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


def test_other_spec_in_diff_does_not_bind(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x=1\n", encoding="utf-8")
    boot = tmp_path / "specs" / "000-bootstrap"
    boot.mkdir(parents=True)
    (boot / "spec.md").write_text("Gate: pass\n", encoding="utf-8")
    real = tmp_path / "specs" / "001"
    real.mkdir(parents=True)
    (real / "spec.md").write_text("Gate: pass\n", encoding="utf-8")
    git_init(tmp_path)
    git_commit(tmp_path, "init")
    (boot / "spec.md").write_text("Gate: pass\n# typo\n", encoding="utf-8")
    (tmp_path / "src" / "b.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.delenv("TEAM_SPEC_ID", raising=False)
    monkeypatch.setattr(
        spec_exists.sys,
        "argv",
        ["spec_exists", "--root", str(tmp_path), "--base", "HEAD"],
    )
    assert spec_exists.main() == 1
