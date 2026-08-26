---
name: review-pr
description: Reviews a spec-branch MR for layering, gates, and spec fidelity. Use on pull requests or git diffs before merge. Does not rewrite AGENTS.md.
---

# 审 MR

看 diff，不看对话态度。

- 有 `spec_id`，且 `specs/<id>/spec.md` 在本次变更或已在仓内。
- `src/` 没有超出 spec 的接口。
- import 方向：models 不向上。
- 新分支有测试。
- 没有把文献综述写进本仓（应停在报告文件 + `card.md`）。
- 没有改 `AGENTS.md`，除非人明确要求。

输出：`Verdict` = APPROVE / COMMENT / REQUEST CHANGES。只写可操作条目。
