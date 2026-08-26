# 作业 001 · 三家 agent 同一条 spec

Cursor / Claude Code / Codex 各自开 worktree，**不要**共用工作区。

```bash
bash scripts/worktree.sh spec/001/cursor
bash scripts/worktree.sh spec/001/claude
bash scripts/worktree.sh spec/001/codex
```

每家只做这件事：

1. 读本目录四份规格。禁止做文献调研。
2. `python3 scripts/team.py new-pkg route_pilot <dest>`（或在已有试点包里做）。
3. 按 `implement-from-spec` 写 `src/`。或对照 `examples/001-makespan/`。
4. `python3 scripts/team.py check --spec 001`
5. 开 MR，标题带 `spec_id: 001`。

完成：三份 MR 都有 `specs/001/spec.md`、四层 `src`、同一套 gates 绿。
