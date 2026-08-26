#!/usr/bin/env python3
"""Fail unless spec.md has the required headings and a Gate line."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED = ("## Goal", "## Interface", "## Tests", "## Out of scope")


def check_spec(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if "Gate:" not in text:
        errors.append(f"{path}: missing 'Gate:' line")
    for heading in REQUIRED:
        if heading not in text:
            errors.append(f"{path}: missing {heading}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default="")
    args = parser.parse_args()
    specs = args.root / "specs"
    if not specs.is_dir():
        print("no specs/; skip heading check")
        return 0
    paths: list[Path]
    if args.spec:
        target = specs / args.spec / "spec.md"
        paths = [target] if target.is_file() else []
        if not paths:
            print(f"missing {target}", file=sys.stderr)
            return 1
    else:
        paths = sorted(specs.glob("*/spec.md"))
    errors: list[str] = []
    for path in paths:
        errors.extend(check_spec(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"ok: {len(paths)} spec.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
