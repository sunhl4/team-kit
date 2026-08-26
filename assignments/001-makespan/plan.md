# plan 001

## models
DurationNs（禁负）。JobId。MakespanNs。

## adapters
无。

## services
`makespan(job, durations) -> {id, summary, makespan_ns}` 或 ValueError。

## entrypoints
`--schema` 与 `run --input json`。成功短字段；失败退出 2。
