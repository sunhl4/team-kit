# team-kit

组内算法包 / 软件包的仓内操作系统。人定题目、审规格、审科学。实现由 Cursor / Claude Code / Codex 写。

## 入口

- Cursor、Codex：读本文件。
- Claude Code：只读 `CLAUDE.md`（已 `@AGENTS.md`）。不要在 `CLAUDE.md` 里另写规矩。
- Skill 只放 `.agents/skills/`。`.claude/skills` 是符号链接。禁止再抄到 `.cursor/skills`。
- 人发给 agent 的默认口令：`做 spec/<id>，用 implement-from-spec`。实现默认走 `do-spec` / `implement-from-spec`。不要发明流程。

## 禁

- **禁止做文献调研或写调研报告。** 那是已有 Skill `academic-paper`（`lit-review`）。没有报告就停，让人先跑那个 Skill。本套件只消费报告，见 `use-lit-report`。
- 没有 `specs/<id>/spec.md` 或 Gate 不是 `pass`，不准改 `src/`。
- 不准在同一笔变更里把 `Gate` 改成 `pass` 并改 `src/`。人先合规格 PR，再让 agent 实现。
- 不准改本文件，除非人在对话里明确要求。
- 一台 agent 只用一个 worktree。分支必须是 `spec/<id>/<slug>`。禁止直推 default。
- 不准改其他 spec 的 Exclusive paths。做完把 `Gate` 标 `done` 才释放路径。

## 命令

```bash
python3 scripts/team.py new-spec <id> <slug>
python3 scripts/team.py new-pkg <module_name> <dest>
python3 scripts/team.py apply <existing_repo>
python3 scripts/team.py apply-assignment 001-makespan <dest> --module <name>
python3 scripts/team.py check
```

完成条件：`team check` 退出码 0；PR 正文 `spec_id` 与分支一致；`--schema` 等于 spec Interface；`tasks.md` 里的 `test_*` 存在；`src/` 落在 Exclusive paths。

## 层

`models` ← `adapters` ← `services` ← `entrypoints`。方向不可反。风格由 ruff / import-linter 执行，不靠口述。
