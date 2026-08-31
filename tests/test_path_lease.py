from pathlib import Path

from gates_loader import load
from gitutil import git_commit, git_init

path_lease = load("path_lease")


def _pkg(root: Path) -> None:
    (root / "src" / "demo").mkdir(parents=True)
    (root / "src" / "demo" / "models").mkdir()
    (root / "src" / "demo" / "models" / "duration.py").write_text("x=1\n", encoding="utf-8")
    spec = root / "specs" / "001"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text("Gate: pass\n", encoding="utf-8")
    (spec / "plan.md").write_text(
        "## Exclusive paths\n\n- src/*/models/duration.py\n",
        encoding="utf-8",
    )


def test_lease_rejects_leak(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path)
    git_init(tmp_path)
    git_commit(tmp_path, "init")
    (tmp_path / "src" / "demo" / "models" / "leak.py").write_text("y=2\n", encoding="utf-8")
    monkeypatch.setattr(
        path_lease.sys,
        "argv",
        ["path_lease", "--root", str(tmp_path), "--spec", "001", "--base", "HEAD"],
    )
    assert path_lease.main() == 1


def test_lease_overlap(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path)
    other = tmp_path / "specs" / "002"
    other.mkdir(parents=True)
    (other / "spec.md").write_text("Gate: pending\n", encoding="utf-8")
    (other / "plan.md").write_text(
        "## Exclusive paths\n\n- src/*/models/duration.py\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        path_lease.sys,
        "argv",
        ["path_lease", "--root", str(tmp_path), "--spec", "001"],
    )
    assert path_lease.main() == 1


def test_done_releases_lease(tmp_path: Path, monkeypatch) -> None:
    _pkg(tmp_path)
    other = tmp_path / "specs" / "002"
    other.mkdir(parents=True)
    (other / "spec.md").write_text("Gate: done\n", encoding="utf-8")
    (other / "plan.md").write_text(
        "## Exclusive paths\n\n- src/*/models/duration.py\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        path_lease.sys,
        "argv",
        ["path_lease", "--root", str(tmp_path), "--spec", "001"],
    )
    assert path_lease.main() == 0
