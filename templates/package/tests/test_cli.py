import json

from {{package_name}}.entrypoints.cli import main


def test_schema(capsys: object) -> None:
    assert main(["--schema"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["required"] == ["id"]


def test_run(capsys: object) -> None:
    assert main(["run", "--input", '{"id":"a"}']) == 0
    assert json.loads(capsys.readouterr().out) == {"id": "a", "summary": "ok"}
