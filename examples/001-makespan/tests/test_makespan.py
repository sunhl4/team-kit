import json

import pytest

from {{package_name}}.entrypoints.cli import main
from {{package_name}}.models.duration import DurationNs, JobId
from {{package_name}}.services.makespan import makespan


def test_sum() -> None:
    out = makespan(JobId("j1"), [DurationNs(10), DurationNs(20), DurationNs(5)])
    assert out["makespan_ns"] == 35


def test_empty() -> None:
    assert makespan(JobId("j2"), [])["makespan_ns"] == 0


def test_negative() -> None:
    with pytest.raises(ValueError):
        DurationNs(-1)


def test_cli_ok(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["run", "--input", '{"id":"j1","durations_ns":[10,20,5]}']) == 0
    assert json.loads(capsys.readouterr().out)["makespan_ns"] == 35


def test_cli_empty(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["run", "--input", '{"id":"j2","durations_ns":[]}']) == 0
    assert json.loads(capsys.readouterr().out)["makespan_ns"] == 0


def test_cli_neg(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["run", "--input", '{"id":"j3","durations_ns":[-1]}']) == 2
    payload = json.loads(capsys.readouterr().out)
    assert "error" in payload["summary"]
    assert "makespan_ns" not in payload
