#!/usr/bin/env bash
# Days 12–14: same spec, same layout, same gates. Any agent must pass this.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKDIR="${1:-$(mktemp -d)}"
MODULE="${2:-route_pilot}"
mkdir -p "$WORKDIR"
DEST="$WORKDIR/$MODULE"
rm -rf "$DEST"
python3 "$ROOT/scripts/team.py" new-pkg "$MODULE" "$DEST"
python3 "$ROOT/scripts/team.py" apply-assignment 001-makespan "$DEST" --module "$MODULE"

# Layout any agent must leave behind
for p in \
  "AGENTS.md" "CLAUDE.md" \
  ".agents/skills/use-lit-report/SKILL.md" \
  ".agents/skills/idea-to-spec/SKILL.md" \
  ".agents/skills/implement-from-spec/SKILL.md" \
  ".agents/skills/do-spec/SKILL.md" \
  "specs/001/spec.md" "specs/001/card.md" \
  "src/$MODULE/models/duration.py" \
  "src/$MODULE/services/makespan.py" \
  "gates/check.sh"
 do
  test -e "$DEST/$p" || { echo "missing $p" >&2; exit 1; }
done
grep -q 'Gate: pass' "$DEST/specs/001/spec.md"
grep -q '@AGENTS.md' "$DEST/CLAUDE.md"

# Unbound src change and path-lease leak → red
(
  cd "$DEST"
  git init -b main >/dev/null
  git add -A
  git -c user.email=kit@local -c user.name=kit commit -m init >/dev/null
  echo 'x = 1' > "src/$MODULE/models/leak.py"
  mv specs/.active /tmp/team-kit-active.$$
  if TEAM_BASE=HEAD TEAM_SPEC_ID= python3 gates/spec_exists.py --root "$DEST"; then
    echo "spec_exists should fail without bound spec_id" >&2
    exit 1
  fi
  mv /tmp/team-kit-active.$$ specs/.active
  if TEAM_BASE=HEAD python3 gates/path_lease.py --root "$DEST" --spec 001; then
    echo "path_lease should reject files outside Exclusive paths" >&2
    exit 1
  fi
  rm -f "src/$MODULE/models/leak.py"
)

(
  cd "$DEST"
  if command -v uv >/dev/null 2>&1; then
    uv venv .venv
    uv pip install -e ".[dev]"
    PATH="$DEST/.venv/bin:$PATH" bash gates/check.sh 001
  else
    python3 -m pip install -e ".[dev]"
    bash gates/check.sh 001
  fi
)
echo "ok: day14 $DEST"
