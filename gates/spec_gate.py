#!/usr/bin/env python3
"""src/ changes require Gate: pass already on the base. Do not stamp pass in the same diff."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    changed_files,
    gate_status_at,
    gate_status_file,
    git,
    has_git,
    resolve_spec_id,
    spec_md,
    src_touched,
)


def _base_ref(root: Path, base: str) -> str:
    merged = git(root, "merge-base", base, "HEAD").strip()
    return merged or base


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=os.environ.get("TEAM_SPEC_ID", ""))
    parser.add_argument("--base", default=os.environ.get("TEAM_BASE", "origin/main"))
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "src").is_dir():
        print("no src/; skip spec-gate")
        return 0

    files: list[str] = []
    if has_git(root):
        files = changed_files(root, args.base)
        if not src_touched(files) and not args.spec:
            print("ok: src/ not in diff")
            return 0

    spec_id = resolve_spec_id(root, args.spec, files)
    if not spec_id:
        if src_touched(files) or args.spec:
            print("cannot bind spec_id for Gate check", file=sys.stderr)
            return 1
        print("ok: no bound spec")
        return 0

    path = spec_md(root, spec_id)
    current = gate_status_file(path)
    if not src_touched(files) and not args.spec:
        print(f"ok: Gate {current or 'missing'} (no src diff)")
        return 0

    if not src_touched(files):
        print(f"ok: {spec_id} Gate {current or 'missing'} (no src diff)")
        return 0

    if current != "pass":
        print(
            f"{path}: src/ or tests/ changed but Gate is {current or 'missing'}; need Gate: pass",
            file=sys.stderr,
        )
        return 1

    if has_git(root):
        base_ref = _base_ref(root, args.base)
        if git(root, "rev-parse", "--verify", base_ref).strip():
            previous = gate_status_at(root, spec_id, base_ref)
            if previous != "pass":
                print(
                    f"{path}: cannot introduce Gate: pass in the same change as src/; "
                    "merge a spec-only PR first",
                    file=sys.stderr,
                )
                return 1

    print(f"ok: {spec_id} Gate: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
