#!/usr/bin/env python3
"""team-kit CLI: new-spec, new-pkg, check."""

from __future__ import annotations

import argparse
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
MODULE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SPEC_RE = re.compile(r"^[0-9A-Za-z][0-9A-Za-z._-]*$")
SKIP_DIR_NAMES = {".git", "__pycache__", ".venv", ".demo", ".ruff_cache", ".pytest_cache"}


def _kit_root() -> Path:
    marker = KIT / "templates" / "package"
    if marker.is_dir():
        return KIT
    here = Path.cwd()
    for parent in (here, *here.parents):
        if (parent / "templates" / "package").is_dir():
            return parent
    return KIT


def _render(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def _copy_tree(src: Path, dest: Path, mapping: dict[str, str] | None = None) -> None:
    mapping = mapping or {}
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in SKIP_DIR_NAMES:
            continue
        target_name = _render(item.name, mapping)
        target = dest / target_name
        if item.is_dir():
            _copy_tree(item, target, mapping)
            continue
        data = item.read_bytes()
        if item.suffix in {".md", ".toml", ".yml", ".yaml", ".sh", ".py", ".ini", ""} or item.name in {
            "AGENTS.md",
            "CLAUDE.md",
            "CODEOWNERS",
            ".gitignore",
            ".importlinter",
        }:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                target.write_bytes(data)
            else:
                target.write_text(_render(text, mapping), encoding="utf-8")
        else:
            target.write_bytes(data)
        if item.suffix == ".sh" or item.name.endswith(".py"):
            target.chmod(target.stat().st_mode | stat.S_IXUSR)


def cmd_new_spec(args: argparse.Namespace) -> int:
    if not SPEC_RE.match(args.spec_id):
        print("spec id must be slug-safe", file=sys.stderr)
        return 2
    root = Path(args.root).resolve()
    dest = root / "specs" / args.spec_id
    if dest.exists() and not args.force:
        print(f"exists: {dest}", file=sys.stderr)
        return 2
    src = _kit_root() / "templates" / "spec"
    dest.mkdir(parents=True, exist_ok=True)
    mapping = {"spec_id": args.spec_id, "slug": args.slug}
    _copy_tree(src, dest, mapping)
    active = root / "specs" / ".active"
    active.write_text(args.spec_id + "\n", encoding="utf-8")
    print(dest)
    return 0


def cmd_new_pkg(args: argparse.Namespace) -> int:
    if not MODULE_RE.match(args.module):
        print("module must be snake_case python name", file=sys.stderr)
        return 2
    dest = Path(args.dest).expanduser().resolve()
    if dest.exists() and any(dest.iterdir()) and not args.force:
        print(f"dest not empty: {dest}", file=sys.stderr)
        return 2
    dest.mkdir(parents=True, exist_ok=True)
    kit = _kit_root()
    mapping = {
        "package_name": args.module,
        "package_dist": args.module.replace("_", "-"),
    }
    _copy_tree(kit / "templates" / "package", dest, mapping)
    for rel in (".agents/skills", "gates", "templates/spec", "config"):
        _copy_tree(kit / rel, dest / rel, mapping)
    (dest / "scripts").mkdir(exist_ok=True)
    shutil.copy2(kit / "scripts" / "team.py", dest / "scripts" / "team.py")
    (dest / "scripts" / "team.py").chmod(
        (dest / "scripts" / "team.py").stat().st_mode | stat.S_IXUSR
    )
    claude = dest / "CLAUDE.md"
    if not claude.exists():
        claude.write_text("@AGENTS.md\n", encoding="utf-8")
    link = dest / ".claude" / "skills"
    link.parent.mkdir(exist_ok=True)
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(Path("../.agents/skills"), target_is_directory=True)
    print(dest)
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    dest = Path(args.dest).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    kit = _kit_root()
    for rel in (".agents/skills", "gates", "templates/spec", "config"):
        _copy_tree(kit / rel, dest / rel)
    (dest / "scripts").mkdir(exist_ok=True)
    shutil.copy2(kit / "scripts" / "team.py", dest / "scripts" / "team.py")
    (dest / "scripts" / "team.py").chmod(
        (dest / "scripts" / "team.py").stat().st_mode | stat.S_IXUSR
    )
    agents = dest / "AGENTS.md"
    if not agents.exists():
        shutil.copy2(kit / "templates" / "package" / "AGENTS.md", agents)
        agents.write_text(
            agents.read_text(encoding="utf-8")
            .replace("{{package_name}}", dest.name.replace("-", "_"))
            .replace("{{package_dist}}", dest.name),
            encoding="utf-8",
        )
    claude = dest / "CLAUDE.md"
    if not claude.exists():
        claude.write_text("@AGENTS.md\n", encoding="utf-8")
    link = dest / ".claude" / "skills"
    link.parent.mkdir(exist_ok=True)
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(Path("../.agents/skills"), target_is_directory=True)
    print(dest)
    return 0


def cmd_apply_assignment(args: argparse.Namespace) -> int:
    kit = _kit_root()
    dest = Path(args.dest).expanduser().resolve()
    src = kit / "assignments" / args.assignment
    example = kit / "examples" / args.assignment
    if not src.is_dir():
        print(f"missing {src}", file=sys.stderr)
        return 2
    spec_id = args.assignment.split("-", 1)[0]
    mapping = {
        "package_name": args.module,
        "package_dist": args.module.replace("_", "-"),
        "spec_id": spec_id,
    }
    _copy_tree(src, dest / "specs" / spec_id, mapping)
    (dest / "specs" / ".active").write_text(spec_id + "\n", encoding="utf-8")
    bootstrap = dest / "specs" / "000-bootstrap" / "spec.md"
    if bootstrap.is_file():
        text = bootstrap.read_text(encoding="utf-8")
        bootstrap.write_text(
            re.sub(r"^Gate:\s*\w+", "Gate: done", text, count=1, flags=re.M),
            encoding="utf-8",
        )
    if example.is_dir():
        pkg = dest / "src" / args.module
        if (example / "models").is_dir():
            _copy_tree(example / "models", pkg / "models", mapping)
        if (example / "services").is_dir():
            _copy_tree(example / "services", pkg / "services", mapping)
        if (example / "entrypoints").is_dir():
            _copy_tree(example / "entrypoints", pkg / "entrypoints", mapping)
        if (example / "tests").is_dir():
            _copy_tree(example / "tests", dest / "tests", mapping)
    print(dest / "specs" / spec_id)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    script = root / "gates" / "check.sh"
    if not script.is_file():
        script = _kit_root() / "gates" / "check.sh"
    cmd = ["bash", str(script)]
    if args.spec:
        cmd.append(args.spec)
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    if args.spec:
        env["TEAM_SPEC_ID"] = args.spec
    return subprocess.call(cmd, cwd=root, env=env)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="team")
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_spec = sub.add_parser("new-spec")
    p_spec.add_argument("spec_id")
    p_spec.add_argument("slug")
    p_spec.add_argument("--root", default=".")
    p_spec.add_argument("--force", action="store_true")
    p_spec.set_defaults(func=cmd_new_spec)

    p_pkg = sub.add_parser("new-pkg")
    p_pkg.add_argument("module")
    p_pkg.add_argument("dest")
    p_pkg.add_argument("--force", action="store_true")
    p_pkg.set_defaults(func=cmd_new_pkg)

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("dest")
    p_apply.set_defaults(func=cmd_apply)

    p_asg = sub.add_parser("apply-assignment")
    p_asg.add_argument("assignment")
    p_asg.add_argument("dest")
    p_asg.add_argument("--module", required=True)
    p_asg.set_defaults(func=cmd_apply_assignment)

    p_check = sub.add_parser("check")
    p_check.add_argument("--root", default=".")
    p_check.add_argument("--spec", default="")
    p_check.set_defaults(func=cmd_check)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
