from pathlib import Path

from gates_loader import GATES
import sys

if str(GATES) not in sys.path:
    sys.path.insert(0, str(GATES))

import common


def test_spec_id_from_branch() -> None:
    assert common.spec_id_from_branch("spec/001/cursor") == "001"
    assert common.spec_id_from_branch("refs/heads/spec/042-a/claude") == "042-a"
    assert common.spec_id_from_branch("main") == ""


def test_spec_id_from_pr_body() -> None:
    body = "## spec\n\n- spec_id: 001\n- Gate: pass\n"
    assert common.spec_id_from_pr_body(body) == "001"
    assert common.spec_id_from_pr_body("nope") == ""


def test_gate_status() -> None:
    assert common.gate_status("Gate: pass\n") == "pass"
    assert common.gate_status("Gate: pending") == "pending"
    assert common.gate_status("Gate: done") == "done"
    assert common.gate_status("Gate: maybe") == ""


def test_parse_exclusive_and_tasks() -> None:
    plan = "## Exclusive paths\n\n- src/*/models/a.py\n- `tests/test_a.py`\n\n## models\n"
    assert common.parse_exclusive_paths(plan) == ["src/*/models/a.py", "tests/test_a.py"]
    tasks = "- [ ] T1 `test_sum` add\n- [ ] T2 team check\n- [ ] T3 no name\n"
    assert common.parse_task_tests(tasks) == ["test_sum"]
    missing = common.task_lines_missing_test_or_check(tasks)
    assert any("T3" in line for line in missing)
    assert not any("T2" in line for line in missing)


def test_path_allowed() -> None:
    pats = ["src/*/models/duration.py", "tests/test_makespan.py"]
    assert common.path_allowed("src/route_pilot/models/duration.py", pats)
    assert not common.path_allowed("src/route_pilot/models/leak.py", pats)
    assert common.path_allowed("src/route_pilot/__init__.py", pats)


def test_parse_interface_schema() -> None:
    text = "## Interface\n\n```json\n{\"type\":\"object\"}\n```\n"
    assert common.parse_interface_schema(text) == {"type": "object"}


def test_resolve_active(tmp_path: Path) -> None:
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / ".active").write_text("001\n", encoding="utf-8")
    assert common.resolve_spec_id(tmp_path) == "001"
