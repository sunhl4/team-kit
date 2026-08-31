#!/usr/bin/env bash
# One agent, one worktree. Usage: bash scripts/worktree.sh spec/001/claude
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${1:?branch spec/<id>/<agent>}"
if [[ ! "$NAME" =~ ^spec/[^/]+/[^/]+$ ]]; then
  echo "branch must be spec/<id>/<slug>" >&2
  exit 2
fi
SAFE="${NAME//\//-}"
DEST="${2:-$ROOT/../team-kit-$SAFE}"
git -C "$ROOT" worktree add -B "$NAME" "$DEST"
echo "$DEST"
