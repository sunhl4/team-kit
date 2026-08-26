#!/usr/bin/env bash
# Require PR + CI on main. Zero approvals so a single owner can merge after green CI.
# Usage: bash scripts/protect_main.sh [owner/repo] [check-name]
set -euo pipefail
REPO="${1:-}"
CHECK="${2:-kit}"
if [[ -z "$REPO" ]]; then
  REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
fi
gh api "repos/${REPO}/rulesets" --method POST --input - <<EOF
{
  "name": "main-no-direct-push",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": false,
        "required_status_checks": [
          {"context": "${CHECK}"}
        ]
      }
    }
  ]
}
EOF
echo "protected ${REPO} main (check=${CHECK})"
