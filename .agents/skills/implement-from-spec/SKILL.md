---
name: implement-from-spec
description: Implements one spec_id into src/ following Cosmic layers and package AGENTS.md. Use only when specs/<id>/spec.md contains Gate: pass.
---

# 按规格实现

1. 读 `specs/<id>/spec.md`。没有 `Gate: pass` 就停，去 `spec-clarity-gate`。
2. 读 `plan.md` 和本仓 `AGENTS.md`。对照已有同层文件再写。
3. 只做 `tasks.md` 里当前任务。一层一个 PR 更好。
4. 层：`models` 无 I/O；`adapters` 不 import `services` / `entrypoints`；`entrypoints` 只解析并调用 `services`。
5. 公开面：CLI `--schema` 与 `run --input json`。短输出：id + summary。
6. 每条 Tests 有对应 pytest。
7. `python3 scripts/team.py check` 或 `bash gates/check.sh` 必须绿。
8. 不要改 `AGENTS.md`。不要扩 Out of scope。
