#!/usr/bin/env python3
"""src/ or tests/ changes must bind to one existing specs/<id>/spec.md."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    changed_files,
    has_git,
    resolve_spec_id,
    spec_md,
    src_touched,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=os.environ.get("TEAM_SPEC_ID", ""))
    parser.add_argument("--base", default=os.environ.get("TEAM_BASE", "origin/main"))
    args = parser.parse_args()
    root = args.root.resolve()
    src = root / "src"
    if not src.is_dir():
        print("no src/; skip spec-exists")
        return 0

    files: list[str] = []
    if has_git(root):
        files = changed_files(root, args.base)
        if not src_touched(files) and not args.spec:
            print("ok: src/ not in diff")
            return 0

    spec_id = resolve_spec_id(root, args.spec, files)
    if not spec_id:
        if not has_git(root) or src_touched(files) or args.spec:
            print("cannot bind spec_id for src/ change", file=sys.stderr)
            return 1
        print("ok: src/ not in diff")
        return 0

    path = spec_md(root, spec_id)
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1
    print(f"ok: {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
