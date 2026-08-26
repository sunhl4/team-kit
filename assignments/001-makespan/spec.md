# spec 001

Gate: pass

## Goal

顺序工序的 `makespan_ns`：输入非负时长列表，输出它们的和。短 JSON，带 `id`。

## Interface

```json
{
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "durations_ns": {
      "type": "array",
      "items": {"type": "integer"}
    }
  },
  "required": ["id", "durations_ns"],
  "additionalProperties": false
}
```

`run` 成功：`{"id":"...","summary":"makespan_ns=<n>","makespan_ns":n}`  
`run` 失败：`{"id":"...","summary":"error: <short>"}`，退出码 2。

## Tests

| id | input | expect |
|----|-------|--------|
| t1 | `{"id":"j1","durations_ns":[10,20,5]}` | `makespan_ns=35`，退出 0 |
| t2 | `{"id":"j2","durations_ns":[]}` | `makespan_ns=0`，退出 0 |
| t3 | `{"id":"j3","durations_ns":[-1]}` | summary 含 `error`，无 `makespan_ns`，退出 2 |

## Out of scope

文献调研。并行 makespan。QVibe / ionstack / twin_id。
