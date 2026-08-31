# plan 001

## Exclusive paths

- src/{{package_name}}/models/duration.py
- src/{{package_name}}/services/makespan.py
- src/{{package_name}}/entrypoints/cli.py
- tests/test_makespan.py
- tests/test_cli.py

## models
DurationNs（禁负）。JobId。MakespanNs。

## adapters
无。

## services
`makespan(job, durations) -> {id, summary, makespan_ns}` 或 ValueError。

## entrypoints
`--schema` 与 `run --input json`。成功短字段；失败退出 2。
