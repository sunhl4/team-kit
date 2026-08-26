#!/usr/bin/env python3
"""If src/ changed vs base, the diff must include specs/<id>/spec.md."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _git(root: Path, *args: str) -> str:
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


def _changed_files(root: Path, base: str) -> list[str]:
    merged = _git(root, "merge-base", base, "HEAD").strip() or base
    text = _git(root, "diff", "--name-only", merged)
    if not text:
        text = _git(root, "diff", "--name-only", "HEAD")
    unstaged = _git(root, "diff", "--name-only")
    staged = _git(root, "diff", "--name-only", "--cached")
    names = set()
    for blob in (text, unstaged, staged):
        names.update(line.strip() for line in blob.splitlines() if line.strip())
    return sorted(names)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=os.environ.get("TEAM_SPEC_ID", ""))
    parser.add_argument(
        "--base",
        default=os.environ.get("TEAM_BASE", "origin/main"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    src = root / "src"
    if not src.is_dir():
        print("no src/; skip spec-exists")
        return 0

    if args.spec:
        spec_md = root / "specs" / args.spec / "spec.md"
        if not spec_md.is_file():
            print(f"missing {spec_md}", file=sys.stderr)
            return 1
        print(f"ok: {spec_md.relative_to(root)}")
        return 0

    if not (root / ".git").exists() and not (root / ".git").is_file():
        specs = list((root / "specs").glob("*/spec.md")) if (root / "specs").is_dir() else []
        if not specs:
            print("src/ present but no specs/*/spec.md", file=sys.stderr)
            return 1
        print(f"ok: {len(specs)} spec.md (no git)")
        return 0

    files = _changed_files(root, args.base)
    src_touched = any(
        f == "src" or f.startswith("src/") or f.startswith("tests/") for f in files
    )
    if not src_touched:
        print("ok: src/ not in diff")
        return 0
    spec_touched = any(
        f.startswith("specs/") and f.endswith("/spec.md") for f in files
    )
    existing = list((root / "specs").glob("*/spec.md")) if (root / "specs").is_dir() else []
    if spec_touched or existing:
        print("ok: spec.md present for src change")
        return 0
    print("src/ or tests/ changed without specs/*/spec.md", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
