#!/usr/bin/env python3
"""Each tasks.md item must name a pytest function that exists, or say check."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    changed_files,
    collect_pytest_names,
    has_git,
    parse_task_tests,
    resolve_spec_id,
    src_touched,
    task_lines_missing_test_or_check,
    tasks_md,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=os.environ.get("TEAM_SPEC_ID", ""))
    parser.add_argument("--base", default=os.environ.get("TEAM_BASE", "origin/main"))
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "src").is_dir():
        print("no src/; skip tasks-match")
        return 0

    files = changed_files(root, args.base) if has_git(root) else []
    spec_id = resolve_spec_id(root, args.spec, files)
    if not spec_id:
        print("ok: no bound spec; skip tasks-match")
        return 0

    path = tasks_md(root, spec_id)
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    errors = [f"{path}: {line}" for line in task_lines_missing_test_or_check(text)]
    have = collect_pytest_names(root / "tests")
    for name in parse_task_tests(text):
        if name not in have:
            errors.append(f"{path}: missing pytest {name}")
    if errors:
        if not src_touched(files) and has_git(root):
            print(f"ok: tasks deferred {spec_id} (no src diff)")
            return 0
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"ok: tasks {spec_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
