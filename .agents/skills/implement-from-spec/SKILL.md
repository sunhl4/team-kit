---
name: implement-from-spec
description: Implements one spec_id into src/ following Cosmic layers and package AGENTS.md. Use only when specs/<id>/spec.md contains Gate: pass.
---

# 按规格实现

1. 读 `specs/<id>/spec.md`。没有 `Gate: pass` 就停，去 `spec-clarity-gate`。不要自己把 Gate 改成 pass。
2. 读 `plan.md`（含 Exclusive paths）和本仓 `AGENTS.md`。对照已有同层文件再写。只动租约里的路径。
3. 只做 `tasks.md` 里当前任务。每条必须有 `test_*` 名或 `check`。一层一个 PR 更好。
4. 层：`models` 无 I/O；`adapters` 不 import `services` / `entrypoints`；`entrypoints` 只解析并调用 `services`。
5. 公开面：CLI `--schema` 必须等于 spec `## Interface` 里的 JSON。`run --input json`。短输出：id + summary。
6. 每条 Tests 有对应 pytest。
7. 分支 `spec/<id>/<slug>`。PR 正文写 `spec_id: <id>`。
8. `python3 scripts/team.py check` 或 `bash gates/check.sh` 必须绿。
9. 不要改 `AGENTS.md`。不要扩 Out of scope。实现合进后把 Gate 标 `done` 才释放路径。
