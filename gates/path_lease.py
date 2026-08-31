#!/usr/bin/env python3
"""This spec's src/tests diff must stay inside plan.md Exclusive paths; active leases disjoint."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    changed_files,
    gate_status_file,
    has_git,
    is_code_path,
    is_shared_code,
    iter_code_files,
    list_spec_ids,
    parse_exclusive_paths,
    path_allowed,
    plan_md,
    resolve_spec_id,
    spec_md,
    src_touched,
)


def _leases(root: Path) -> dict[str, list[str]]:
    held: dict[str, list[str]] = {}
    for spec_id in list_spec_ids(root):
        status = gate_status_file(spec_md(root, spec_id))
        if status not in {"pending", "pass"}:
            continue
        path = plan_md(root, spec_id)
        if not path.is_file():
            continue
        held[spec_id] = parse_exclusive_paths(path.read_text(encoding="utf-8"))
    return held


def _overlap(root: Path, left: list[str], right: list[str]) -> list[str]:
    hits: set[str] = set(left) & set(right)
    for file_path in iter_code_files(root):
        if path_allowed(file_path, left) and path_allowed(file_path, right):
            if not is_shared_code(file_path):
                hits.add(file_path)
    return sorted(hits)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=os.environ.get("TEAM_SPEC_ID", ""))
    parser.add_argument("--base", default=os.environ.get("TEAM_BASE", "origin/main"))
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "src").is_dir():
        print("no src/; skip path-lease")
        return 0

    files = changed_files(root, args.base) if has_git(root) else []
    spec_id = resolve_spec_id(root, args.spec, files)
    if not spec_id:
        if src_touched(files):
            print("cannot bind spec_id for path lease", file=sys.stderr)
            return 1
        print("ok: no bound spec; skip path-lease")
        return 0

    plan = plan_md(root, spec_id)
    if not plan.is_file():
        print(f"missing {plan}", file=sys.stderr)
        return 1
    patterns = parse_exclusive_paths(plan.read_text(encoding="utf-8"))
    if src_touched(files) and not patterns:
        print(f"{plan}: ## Exclusive paths is empty while src/ changed", file=sys.stderr)
        return 1

    leaked = [
        item
        for item in files
        if is_code_path(item) and not is_shared_code(item) and not path_allowed(item, patterns)
    ]
    if leaked:
        print(
            f"{plan}: files outside Exclusive paths: {', '.join(leaked)}",
            file=sys.stderr,
        )
        return 1

    held = _leases(root)
    mine = held.get(spec_id, patterns)
    for other, other_paths in held.items():
        if other == spec_id:
            continue
        clash = _overlap(root, mine, other_paths)
        if clash:
            print(
                f"path lease overlap {spec_id} vs {other}: {', '.join(clash)}",
                file=sys.stderr,
            )
            return 1

    print(f"ok: lease {spec_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
