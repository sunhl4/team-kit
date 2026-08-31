#!/usr/bin/env python3
"""CLI --schema must equal the JSON fence under ## Interface in the bound spec."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    changed_files,
    cli_schema,
    find_package_module,
    has_git,
    parse_interface_schema,
    resolve_spec_id,
    schemas_equal,
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
    if not (root / "src").is_dir():
        print("no src/; skip schema-match")
        return 0

    files = changed_files(root, args.base) if has_git(root) else []
    spec_id = resolve_spec_id(root, args.spec, files)
    if not spec_id:
        print("ok: no bound spec; skip schema-match")
        return 0

    path = spec_md(root, spec_id)
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1
    expected = parse_interface_schema(path.read_text(encoding="utf-8"))
    if expected is None:
        print(f"{path}: missing JSON fence under ## Interface", file=sys.stderr)
        return 1

    module = find_package_module(root)
    if not module:
        print("no package under src/; skip schema-match")
        return 0
    try:
        actual = cli_schema(root, module)
    except (RuntimeError, ValueError) as exc:
        print(f"cli --schema failed: {exc}", file=sys.stderr)
        return 1
    if not schemas_equal(expected, actual):
        if src_touched(files) or not has_git(root):
            print(
                f"{path}: Interface JSON != {module} --schema",
                file=sys.stderr,
            )
            return 1
        print(f"ok: schema deferred {spec_id} (no src diff)")
        return 0
    print(f"ok: schema {spec_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
