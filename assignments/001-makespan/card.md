# card 001

## Source
- kind: idea
- report:
- skill: idea-to-spec
- agents: Cursor / Claude Code / Codex 必须产出同一目录形状

## Claims
- 顺序调度的 makespan 等于各段时长之和。

## Algorithm
- 名字：sequential makespan
- 输入：`id`，`durations_ns`（非负整数列表）
- 输出：`makespan_ns` = sum
- 复杂度：O(n)

## Interface
- CLI：`--schema`；`run --input '{"id":"j1","durations_ns":[10,20,5]}'`

## Test vectors
- `{"id":"j1","durations_ns":[10,20,5]}` → `makespan_ns=35`
- `{"id":"j2","durations_ns":[]}` → `makespan_ns=0`
- `{"id":"j3","durations_ns":[-1]}` → error，不写 makespan_ns

## Out of scope
- 文献调研。并行调度 / critical path。Shuttle / CAL。TwinRun。
