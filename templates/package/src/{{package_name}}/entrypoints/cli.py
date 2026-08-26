from __future__ import annotations

import argparse
import json

from {{package_name}}.models.identity import PackageId
from {{package_name}}.services.health import health

SCHEMA: dict = {
    "type": "object",
    "properties": {"id": {"type": "string"}},
    "required": ["id"],
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
    result = health(PackageId(str(payload["id"])))
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
