# {{package_name}}

算法 / 软件包。实现走 Skill。人审规格与科学。

## 入口

Cursor / Codex 读本文件。Claude Code 读 `CLAUDE.md`（`@AGENTS.md`）。Skill 在 `.agents/skills/`。

## 禁

- 文献调研用已有 `academic-paper`（lit-review）。本仓只消费报告：`use-lit-report`。
- 无 `specs/<id>/spec.md` 且无 `Gate: pass` 时不准改 `src/`。
- 不准改本文件，除非人明确要求。
- 一 agent 一 worktree。分支 `spec/<id>/<slug>`。

## 命令

```bash
python3 scripts/team.py new-spec <id> <slug>
python3 scripts/team.py check
{{package_name}} --schema
{{package_name}} run --input '{"id":"x"}'
```

层：`models` ← `adapters` ← `services` ← `entrypoints`。门禁：`bash gates/check.sh`。
