---
name: use-lit-report
description: Consumes an existing literature-survey report and writes specs/<id>/card.md. Use after academic-paper lit-review (or any finished 文献调研报告). Do not search, screen, or write a survey.
---

# 消费已有文献报告

**禁止**检索、筛选、写综述。那是 `academic-paper` 的 `lit-review`（路径见 `config/external-skills.toml`）。

## 没有报告

停。告诉人去跑已有文献 Skill。不要在本仓补调研。

## 有报告

1. 读报告全文。不要重写报告。
2. `python3 scripts/team.py new-spec <id> <slug>`（目录已存在则跳过）。
3. 只填 `specs/<id>/card.md`：

```markdown
# card <id>

## Source
- report: <path>
- skill: academic-paper / lit-review

## Claims
- 一条可证伪的主张（含出处）

## Algorithm
- 名字、输入、输出、复杂度（写未知就写未知）

## Interface
- 函数或 CLI 形状，短

## Test vectors
- 至少两条：输入 → 期望（可先标 TODO 但必须可测）

## Out of scope
- 报告里有、本包不做的
```

4. 不要写 `src/`。下一步是 `spec-clarity-gate`。
