from __future__ import annotations

import argparse
import json

from {{package_name}}.models.duration import DurationNs, JobId
from {{package_name}}.services.makespan import makespan

SCHEMA: dict = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "durations_ns": {"type": "array", "items": {"type": "integer"}},
    },
    "required": ["id", "durations_ns"],
    "additionalProperties": False,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="{{package_name}}")
    parser.add_argument("--schema", action="store_true")
    sub = parser.add_subparsers(dest="cmd")
    run = sub.add_parser("run")
    run.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    if args.schema:
        print(json.dumps(SCHEMA, separators=(",", ":")))
        return 0
    if args.cmd != "run":
        parser.print_help()
        return 2
    payload = json.loads(args.input)
    job_id = str(payload["id"])
    try:
        job = JobId(job_id)
        durations = [DurationNs(int(item)) for item in payload["durations_ns"]]
        result = makespan(job, durations)
    except (KeyError, TypeError, ValueError) as exc:
        print(
            json.dumps(
                {"id": job_id, "summary": f"error: {exc}"}, separators=(",", ":")
            )
        )
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
