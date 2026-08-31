from __future__ import annotations

import subprocess
from pathlib import Path


def git_init(root: Path) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "kit@local"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "kit"], cwd=root, check=True, capture_output=True)


def git_commit(root: Path, message: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", message], cwd=root, check=True, capture_output=True)
