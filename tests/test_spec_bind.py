from pathlib import Path

from gates_loader import load
from gitutil import git_commit, git_init

spec_bind = load("spec_bind")


def test_require_branch_and_pr(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x=1\n", encoding="utf-8")
    spec = tmp_path / "specs" / "001"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text("Gate: pass\n", encoding="utf-8")
    git_init(tmp_path)
    git_commit(tmp_path, "init")
    (tmp_path / "src" / "b.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.setenv("TEAM_REQUIRE_BRANCH", "1")
    monkeypatch.setenv("TEAM_REQUIRE_PR_SPEC", "1")
    monkeypatch.setenv("TEAM_HEAD_REF", "docs/nope")
    monkeypatch.setenv("TEAM_PR_BODY", "")
    monkeypatch.setattr(
        spec_bind.sys,
        "argv",
        ["spec_bind", "--root", str(tmp_path), "--spec", "001", "--base", "HEAD"],
    )
    assert spec_bind.main() == 1

    monkeypatch.setenv("TEAM_HEAD_REF", "spec/001/cursor")
    monkeypatch.setenv("TEAM_PR_BODY", "- spec_id: 001\n")
    assert spec_bind.main() == 0


def test_pr_spec_mismatch(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x=1\n", encoding="utf-8")
    spec = tmp_path / "specs" / "001"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text("Gate: pass\n", encoding="utf-8")
    git_init(tmp_path)
    git_commit(tmp_path, "init")
    (tmp_path / "src" / "b.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.setenv("TEAM_REQUIRE_BRANCH", "1")
    monkeypatch.setenv("TEAM_REQUIRE_PR_SPEC", "1")
    monkeypatch.setenv("TEAM_HEAD_REF", "spec/001/cursor")
    monkeypatch.setenv("TEAM_PR_BODY", "- spec_id: 002\n")
    monkeypatch.setattr(
        spec_bind.sys,
        "argv",
        ["spec_bind", "--root", str(tmp_path), "--spec", "001", "--base", "HEAD"],
    )
    assert spec_bind.main() == 1
