---
name: spec-clarity-gate
description: Judges whether specs/<id>/spec.md is testable enough to allow src/ edits. Use before implementation, after card or idea spec exists.
---

# 规格门

跑：

```bash
python3 scripts/team.py check --spec <id>
```

人工再问四句，任一为否就停，只改 `specs/<id>/`，不准动 `src/`：

1. 接口能否写成 JSON Schema？
2. 每条 Tests 是否有输入和期望？
3. 失败时返回什么，写了没有？
4. Out of scope 是否排除了「顺便做」的功能？

过关：在 `specs/<id>/spec.md` 文首加一行 `Gate: pass`。
