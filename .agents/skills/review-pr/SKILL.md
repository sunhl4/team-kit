---
name: review-pr
description: Reviews a spec-branch MR for layering, gates, and spec fidelity. Use on pull requests or git diffs before merge. Does not rewrite AGENTS.md.
---

# 审 MR

看 diff，不看对话态度。

- PR 正文 `spec_id` 与分支 `spec/<id>/` 一致。
- 改 `src/` 时 Gate 已是 `pass`，且本 PR 没有把 Gate 改成 pass。
- `src/` 落在 Exclusive paths；`--schema` 对 Interface；tasks 的 `test_*` 存在。
- import 方向：models 不向上。
- 新分支有测试。
- 没有把文献综述写进本仓（应停在报告文件 + `card.md`）。
- 没有改 `AGENTS.md`，除非人明确要求。

输出：`Verdict` = APPROVE / COMMENT / REQUEST CHANGES。只写可操作条目。
