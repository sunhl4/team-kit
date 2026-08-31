#!/usr/bin/env python3
"""CI: branch spec/<id>/<slug> and PR spec_id must match the bound spec."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    changed_files,
    current_branch,
    has_git,
    require_flag,
    resolve_spec_id,
    spec_id_from_branch,
    spec_id_from_pr_body,
    src_touched,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=os.environ.get("TEAM_SPEC_ID", ""))
    parser.add_argument("--base", default=os.environ.get("TEAM_BASE", "origin/main"))
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "src").is_dir():
        print("no src/; skip spec-bind")
        return 0

    files: list[str] = []
    if has_git(root):
        files = changed_files(root, args.base)
        if not src_touched(files) and not require_flag("TEAM_REQUIRE_BRANCH"):
            print("ok: src/ not in diff")
            return 0

    spec_id = resolve_spec_id(root, args.spec, files)
    branch = current_branch(root)
    branch_id = spec_id_from_branch(branch)
    body = os.environ.get("TEAM_PR_BODY", "")
    body_id = spec_id_from_pr_body(body)

    if require_flag("TEAM_REQUIRE_BRANCH") and src_touched(files):
        if not branch_id:
            print(
                f"branch {branch!r} must be spec/<id>/<slug> when src/ changes",
                file=sys.stderr,
            )
            return 1
        if spec_id and branch_id != spec_id:
            print(
                f"branch spec id {branch_id} != bound spec_id {spec_id}",
                file=sys.stderr,
            )
            return 1

    if require_flag("TEAM_REQUIRE_PR_SPEC") and src_touched(files):
        if not body_id:
            print("PR body must contain spec_id: <id>", file=sys.stderr)
            return 1
        want = spec_id or branch_id
        if want and body_id != want:
            print(f"PR spec_id {body_id} != {want}", file=sys.stderr)
            return 1

    print(f"ok: bind {spec_id or branch_id or 'n/a'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
