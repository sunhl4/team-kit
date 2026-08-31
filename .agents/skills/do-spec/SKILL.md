---
name: do-spec
description: Default team command. When the user says 做 spec/<id> or implement spec <id>, run implement-from-spec. Do not invent a workflow or write src/ if Gate is not pass.
---

# 做 spec

人口令：「做 spec/<id>，用 implement-from-spec」。

1. 读 `specs/<id>/spec.md`。Gate 不是 `pass` 就停，去 `spec-clarity-gate`。不要自己写 `Gate: pass`。
2. 其余步骤与 `implement-from-spec` 相同。
3. 不要跳过 `plan.md` 的 Exclusive paths，也不要跳过 `tasks.md` 里的 `test_*` 名。
