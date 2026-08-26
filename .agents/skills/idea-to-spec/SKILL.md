---
name: idea-to-spec
description: Turns a new project or algorithm idea into specs/<id>/ files. Use when there is no literature report and the user wants a software or algorithm package from an idea.
---

# 想法 → 规格

1. `python3 scripts/team.py new-spec <id> <slug>`
2. 填四个文件，不要先写代码：

| 文件 | 只写 |
|------|------|
| `card.md` | 一句话目标、非目标 |
| `spec.md` | 行为、接口 JSON Schema、错误、完成条件 |
| `plan.md` | 四层各放什么（models / adapters / services / entrypoints） |
| `tasks.md` | 可单独测的任务，一条一个测试 |

3. `spec.md` 必须有这些标题：`Goal` `Interface` `Tests` `Out of scope`。
4. 停。等人跑 `spec-clarity-gate`。
