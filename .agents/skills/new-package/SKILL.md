---
name: new-package
description: Instantiates a Cosmic-layered Python package from team-kit. Use when creating a new algorithm or software package repository, never mkdir a blank tree.
---

# 新包

不要空白 `mkdir`。

新仓：

```bash
python3 scripts/team.py new-pkg <module_name> <dest>
```

已有仓只接线，不覆盖已有 `AGENTS.md`：

```bash
python3 scripts/team.py apply <existing_repo>
```

`<module_name>` 必须是 `snake_case`。`<dest>` 是新仓目录。

做完检查：

- `<dest>/AGENTS.md`、`CLAUDE.md`、`.agents/skills/`、`.claude/skills` 都在
- `cd <dest> && python3 -c "import scripts"` 不必；用套件里拷过去的 `python3 scripts/team.py check` 或包内 `bash gates/check.sh`
- 新仓第一笔提交可以带 `specs/000-bootstrap/spec.md`（模板已带）

然后用 `implement-from-spec`。本 Skill 不写业务代码。
