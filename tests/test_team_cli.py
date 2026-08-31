from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEAM = Path(__file__).resolve().parents[1] / "scripts" / "team.py"


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TEAM), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def test_new_spec(tmp_path: Path) -> None:
    out = _run("new-spec", "042", "demo", "--root", str(tmp_path))
    assert out.returncode == 0, out.stderr
    spec = tmp_path / "specs" / "042" / "spec.md"
    assert spec.is_file()
    assert "## Goal" in spec.read_text(encoding="utf-8")
    assert "## Exclusive paths" in (tmp_path / "specs" / "042" / "plan.md").read_text(
        encoding="utf-8"
    )
    assert (tmp_path / "specs" / ".active").read_text(encoding="utf-8").strip() == "042"


def test_new_pkg_and_import(tmp_path: Path) -> None:
    dest = tmp_path / "demo_pkg"
    out = _run("new-pkg", "demo_pkg", str(dest))
    assert out.returncode == 0, out.stderr
    assert (dest / "AGENTS.md").is_file()
    assert (dest / ".agents" / "skills" / "use-lit-report" / "SKILL.md").is_file()
    assert (dest / ".agents" / "skills" / "do-spec" / "SKILL.md").is_file()
    assert (dest / ".claude" / "skills").is_symlink()
    init = (dest / "src" / "demo_pkg" / "__init__.py").read_text(encoding="utf-8")
    assert "from demo_pkg.models.identity import PackageId" in init
    assert (dest / "specs" / "000-bootstrap" / "spec.md").is_file()
    assert "use-lit-report" in (dest / ".agents" / "skills" / "use-lit-report" / "SKILL.md").read_text(
        encoding="utf-8"
    )


def test_apply_existing(tmp_path: Path) -> None:
    repo = tmp_path / "old"
    repo.mkdir()
    (repo / "AGENTS.md").write_text("keep\n", encoding="utf-8")
    out = _run("apply", str(repo))
    assert out.returncode == 0, out.stderr
    assert (repo / "AGENTS.md").read_text(encoding="utf-8") == "keep\n"
    assert (repo / ".agents" / "skills" / "idea-to-spec" / "SKILL.md").is_file()
    assert (repo / "CLAUDE.md").read_text(encoding="utf-8").startswith("@AGENTS.md")
