"""Shared helpers for team-kit gates. Stdlib only."""

from __future__ import annotations

import ast
import fnmatch
import json
import os
import re
import subprocess
from pathlib import Path

GATE_RE = re.compile(r"^Gate:\s*(pending|pass|done)\s*$", re.MULTILINE)
BRANCH_SPEC_RE = re.compile(r"^(?:refs/heads/)?spec/([0-9A-Za-z._-]+)/")
PR_SPEC_RE = re.compile(r"(?im)^(?:\s*-\s*)?spec_id:\s*([0-9A-Za-z._-]+)\s*$")
TEST_NAME_RE = re.compile(r"\b(test_[A-Za-z0-9_]+)\b")
JSON_FENCE_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)

CODE_PREFIXES = ("src/", "tests/")


def git(root: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if out.returncode != 0:
        return ""
    return out.stdout


def has_git(root: Path) -> bool:
    return (root / ".git").exists() or (root / ".git").is_file()


def changed_files(root: Path, base: str) -> list[str]:
    merged = git(root, "merge-base", base, "HEAD").strip() or base
    text = git(root, "diff", "--name-only", merged)
    if not text:
        text = git(root, "diff", "--name-only", "HEAD")
    unstaged = git(root, "diff", "--name-only")
    staged = git(root, "diff", "--name-only", "--cached")
    untracked = git(root, "ls-files", "--others", "--exclude-standard")
    names: set[str] = set()
    for blob in (text, unstaged, staged, untracked):
        names.update(line.strip() for line in blob.splitlines() if line.strip())
    return sorted(names)


def is_code_path(path: str) -> bool:
    return path == "src" or path.startswith(CODE_PREFIXES)


def src_touched(files: list[str]) -> bool:
    return any(is_code_path(item) for item in files)


def is_shared_code(path: str) -> bool:
    return path.endswith("/__init__.py") or path.endswith("/__main__.py")


def current_branch(root: Path) -> str:
    env = os.environ.get("TEAM_HEAD_REF", "").strip()
    if env:
        return env
    return git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()


def spec_id_from_branch(branch: str) -> str:
    match = BRANCH_SPEC_RE.match(branch.strip())
    return match.group(1) if match else ""


def spec_id_from_pr_body(body: str) -> str:
    match = PR_SPEC_RE.search(body or "")
    return match.group(1) if match else ""


def read_active(root: Path) -> str:
    path = root / "specs" / ".active"
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return ""


def list_spec_ids(root: Path) -> list[str]:
    specs = root / "specs"
    if not specs.is_dir():
        return []
    ids: list[str] = []
    for item in sorted(specs.iterdir()):
        if item.is_dir() and (item / "spec.md").is_file():
            ids.append(item.name)
    return ids


def resolve_spec_id(
    root: Path,
    explicit: str = "",
    files: list[str] | None = None,
) -> str:
    if explicit.strip():
        return explicit.strip()
    env = os.environ.get("TEAM_SPEC_ID", "").strip()
    if env:
        return env
    from_branch = spec_id_from_branch(current_branch(root))
    if from_branch:
        return from_branch
    active = read_active(root)
    if active:
        return active
    ids = list_spec_ids(root)
    if len(ids) == 1:
        return ids[0]
    return ""


def spec_md(root: Path, spec_id: str) -> Path:
    return root / "specs" / spec_id / "spec.md"


def plan_md(root: Path, spec_id: str) -> Path:
    return root / "specs" / spec_id / "plan.md"


def tasks_md(root: Path, spec_id: str) -> Path:
    return root / "specs" / spec_id / "tasks.md"


def gate_status(text: str) -> str:
    match = GATE_RE.search(text)
    return match.group(1) if match else ""


def gate_status_file(path: Path) -> str:
    if not path.is_file():
        return ""
    return gate_status(path.read_text(encoding="utf-8"))


def gate_status_at(root: Path, spec_id: str, ref: str) -> str:
    blob = git(root, "show", f"{ref}:{Path('specs') / spec_id / 'spec.md'}")
    return gate_status(blob) if blob else ""


def parse_interface_schema(text: str) -> object | None:
    heading = text.find("## Interface")
    body = text[heading:] if heading >= 0 else text
    match = JSON_FENCE_RE.search(body)
    if not match:
        return None
    return json.loads(match.group(1))


def _section_after(text: str, heading: str) -> str:
    marker = heading if heading.startswith("## ") else f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker) :]
    nxt = re.search(r"^## ", rest, flags=re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def parse_exclusive_paths(plan_text: str) -> list[str]:
    section = _section_after(plan_text, "## Exclusive paths")
    if not section.strip():
        return []
    paths: list[str] = []
    in_fence = False
    for raw in section.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        line = line.strip("`")
        if line:
            paths.append(line)
    return paths


def parse_task_tests(tasks_text: str) -> list[str]:
    names: list[str] = []
    for line in tasks_text.splitlines():
        if line.lstrip().startswith("-"):
            names.extend(TEST_NAME_RE.findall(line))
    return names


def task_lines_missing_test_or_check(tasks_text: str) -> list[str]:
    missing: list[str] = []
    for raw in tasks_text.splitlines():
        line = raw.strip()
        if not line.startswith("-"):
            continue
        if TEST_NAME_RE.search(line):
            continue
        if re.search(r"\bcheck\b", line, flags=re.IGNORECASE):
            continue
        missing.append(line)
    return missing


def collect_pytest_names(tests_root: Path) -> set[str]:
    names: set[str] = set()
    if not tests_root.is_dir():
        return names
    for path in tests_root.rglob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                names.add(node.name)
    return names


def path_allowed(path: str, patterns: list[str]) -> bool:
    if is_shared_code(path):
        return True
    for pattern in patterns:
        if path == pattern or path.startswith(pattern.rstrip("/") + "/"):
            return True
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def iter_code_files(root: Path) -> list[str]:
    found: list[str] = []
    for folder in ("src", "tests"):
        base = root / folder
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                found.append(str(path.relative_to(root)).replace("\\", "/"))
    return found


def find_package_module(root: Path) -> str:
    src = root / "src"
    if not src.is_dir():
        return ""
    for item in sorted(src.iterdir()):
        if item.is_dir() and (item / "__init__.py").is_file():
            return item.name
    return ""


def cli_schema(root: Path, module: str) -> object:
    env = dict(os.environ)
    src = str(root / "src")
    env["PYTHONPATH"] = src + os.pathsep + env.get("PYTHONPATH", "")
    code = (
        "import json, sys\n"
        f"from {module}.entrypoints.cli import main\n"
        "raise SystemExit(main(['--schema']))\n"
    )
    out = subprocess.run(
        [os.environ.get("PYTHON", "python3"), "-c", code],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or out.stdout.strip() or "cli --schema failed")
    return json.loads(out.stdout)


def schemas_equal(left: object, right: object) -> bool:
    return json.loads(json.dumps(left)) == json.loads(json.dumps(right))


def require_flag(name: str) -> bool:
    return os.environ.get(name, "").strip() in {"1", "true", "yes"}
