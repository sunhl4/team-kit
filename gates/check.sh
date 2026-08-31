#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
SPEC="${1:-${TEAM_SPEC_ID:-}}"

python3 "$ROOT/gates/spec_exists.py" --root "$ROOT" ${SPEC:+--spec "$SPEC"}
python3 "$ROOT/gates/spec_headings.py" --root "$ROOT" ${SPEC:+--spec "$SPEC"}
python3 "$ROOT/gates/spec_gate.py" --root "$ROOT" ${SPEC:+--spec "$SPEC"}
python3 "$ROOT/gates/spec_bind.py" --root "$ROOT" ${SPEC:+--spec "$SPEC"}

if [[ -d "$ROOT/src" ]]; then
  python3 "$ROOT/gates/schema_match.py" --root "$ROOT" ${SPEC:+--spec "$SPEC"}
  python3 "$ROOT/gates/tasks_match.py" --root "$ROOT" ${SPEC:+--spec "$SPEC"}
  python3 "$ROOT/gates/path_lease.py" --root "$ROOT" ${SPEC:+--spec "$SPEC"}

  python3 -m ruff format --check "$ROOT/src" "$ROOT/tests"
  python3 -m ruff check "$ROOT/src" "$ROOT/tests"
  if [[ -f "$ROOT/.importlinter" ]]; then
    command -v lint-imports >/dev/null || {
      echo "lint-imports missing; pip install '.[dev]'" >&2
      exit 1
    }
    (cd "$ROOT" && lint-imports)
  fi
  python3 -m pytest -q
fi
echo "ok: gates"
