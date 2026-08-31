from pathlib import Path

from gates_loader import load
from gitutil import git_commit, git_init

spec_gate = load("spec_gate")


def _pkg(root: Path, gate: str) -> None:
    (root / "src").mkdir()
    (root / "src" / "a.py").write_text("x=1\n", encoding="utf-8")
    spec = root / "specs" / "001"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text(
        f"# spec 001\n\nGate: {gate}\n\n## Goal\n\n## Interface\n\n## Tests\n\n## Out of scope\n",
        encoding="utf-8",
    )


def test_pending_blocks_src(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path, "pending")
    git_init(tmp_path)
    git_commit(tmp_path, "spec")
    (tmp_path / "src" / "b.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.setattr(
        spec_gate.sys,
        "argv",
        ["spec_gate", "--root", str(tmp_path), "--spec", "001", "--base", "HEAD"],
    )
    assert spec_gate.main() == 1


def test_stamp_pass_with_src_fails(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path, "pending")
    git_init(tmp_path)
    git_commit(tmp_path, "spec pending")
    (tmp_path / "specs" / "001" / "spec.md").write_text(
        "# spec 001\n\nGate: pass\n\n## Goal\n\n## Interface\n\n## Tests\n\n## Out of scope\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "b.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.setattr(
        spec_gate.sys,
        "argv",
        ["spec_gate", "--root", str(tmp_path), "--spec", "001", "--base", "HEAD"],
    )
    assert spec_gate.main() == 1


def test_missing_remote_base_skips_twostep(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path, "pass")
    git_init(tmp_path)
    git_commit(tmp_path, "local only")
    (tmp_path / "src" / "b.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.setattr(
        spec_gate.sys,
        "argv",
        ["spec_gate", "--root", str(tmp_path), "--spec", "001", "--base", "origin/main"],
    )
    assert spec_gate.main() == 0


def test_pass_already_on_base_allows_src(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path, "pass")
    git_init(tmp_path)
    git_commit(tmp_path, "gate pass")
    (tmp_path / "src" / "b.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.setattr(
        spec_gate.sys,
        "argv",
        ["spec_gate", "--root", str(tmp_path), "--spec", "001", "--base", "HEAD"],
    )
    assert spec_gate.main() == 0
