from pathlib import Path

from gates_loader import load

tasks_match = load("tasks_match")


def test_tasks_ok_and_missing(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "src").mkdir()
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_foo.py").write_text("def test_sum():\n    assert True\n", encoding="utf-8")
    spec = tmp_path / "specs" / "001"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text("Gate: pass\n", encoding="utf-8")
    (spec / "tasks.md").write_text(
        "# tasks\n\n- [ ] T1 `test_sum` add\n- [ ] T2 team check\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        tasks_match.sys,
        "argv",
        ["tasks_match", "--root", str(tmp_path), "--spec", "001"],
    )
    assert tasks_match.main() == 0

    (spec / "tasks.md").write_text("- [ ] T1 `test_missing`\n", encoding="utf-8")
    assert tasks_match.main() == 1
