from pathlib import Path

from test_team_cli import TEAM, _run


def test_apply_assignment(tmp_path: Path) -> None:
    dest = tmp_path / "route_pilot"
    assert _run("new-pkg", "route_pilot", str(dest)).returncode == 0
    out = _run(
        "apply-assignment",
        "001-makespan",
        str(dest),
        "--module",
        "route_pilot",
    )
    assert out.returncode == 0, out.stderr
    spec = dest / "specs" / "001" / "spec.md"
    assert "Gate: pass" in spec.read_text(encoding="utf-8")
    cli = (dest / "src" / "route_pilot" / "entrypoints" / "cli.py").read_text(
        encoding="utf-8"
    )
    assert "from route_pilot.services.makespan import makespan" in cli
    assert (dest / "tests" / "test_makespan.py").is_file()
