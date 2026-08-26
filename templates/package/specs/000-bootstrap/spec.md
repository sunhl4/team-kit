# spec 000-bootstrap

Gate: pass

## Goal

Skeleton package: identity + health CLI. Replace this spec when real work starts.

## Interface

```json
{
  "type": "object",
  "properties": {"id": {"type": "string"}},
  "required": ["id"],
  "additionalProperties": false
}
```

## Tests

| id | input | expect |
|----|-------|--------|
| t1 | `{"id":"a"}` | `{"id":"a","summary":"ok"}` |

## Out of scope

Business algorithms. Literature survey.
