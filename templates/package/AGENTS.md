# {{package_name}}

算法 / 软件包。实现走 Skill。人审规格与科学。

## 入口

Cursor / Codex 读本文件。Claude Code 读 `CLAUDE.md`（`@AGENTS.md`）。Skill 在 `.agents/skills/`。

人发给 agent 的默认口令：`做 spec/<id>，用 implement-from-spec`。不要发明流程。

## 禁

- 文献调研用已有 `academic-paper`（lit-review）。本仓只消费报告：`use-lit-report`。
- 无 `specs/<id>/spec.md` 或 Gate 不是 `pass` 时不准改 `src/`。
- 不准在同一笔变更里把 `Gate` 改成 `pass` 并改 `src/`。
- 不准改本文件，除非人明确要求。
- 一 agent 一 worktree。分支必须是 `spec/<id>/<slug>`。
- `src/` 只能落在本 spec `plan.md` 的 Exclusive paths。

## 命令

```bash
python3 scripts/team.py new-spec <id> <slug>
python3 scripts/team.py check
{{package_name}} --schema
{{package_name}} run --input '{"id":"x"}'
```

完成条件：`team check` 绿；PR 有 `spec_id`；`--schema` 对得上 Interface；tasks 测试名存在。

层：`models` ← `adapters` ← `services` ← `entrypoints`。门禁：`bash gates/check.sh`。
