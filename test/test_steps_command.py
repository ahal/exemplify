import inspect

import pytest

from exemplify.util import process


@pytest.fixture(autouse=True)
def patch_verbose(request, monkeypatch):
    monkeypatch.setattr(process, "VERBOSE", True)


@pytest.mark.parametrize(
    "kwargs,expected_returncode,expected_output",
    (
        pytest.param(
            {"run": "echo hello"},
            0,
            ["hello"],
            id="string",
        ),
        pytest.param(
            {"run": ["echo hello", "echo goodbye"]},
            0,
            ["hello", "", "goodbye"],
            id="list",
        ),
        pytest.param(
            {"run": "true && echo test"},
            0,
            ["test"],
            id="success && success",
        ),
        pytest.param(
            {"run": "false && echo test"},
            1,
            [],
            id="fail && success",
        ),
        pytest.param(
            {"run": "echo hello | cut -d'e' -f1"},
            0,
            ["h"],
            id="pipe",
        ),
    ),
)
def test_command_sync(capfd, make_step, kwargs, expected_returncode, expected_output):
    step = make_step(**kwargs)
    if inspect.isclass(expected_output) and issubclass(expected_output, Exception):
        with pytest.raises(expected_output):
            step.sync()
    else:
        ret = step.sync()
        out, _ = capfd.readouterr()
        capfd.disabled()
        assert ret == expected_returncode
        assert [line.strip() for line in out.strip().splitlines()] == expected_output


@pytest.mark.parametrize(
    "kwargs,expected_directive",
    (
        pytest.param(
            {"run": "echo hello", "cwd": "workdir"},
            "echo hello",
            id="default",
        ),
        pytest.param(
            {"run": "echo hello", "alias": "printing hello"},
            "printing hello",
            id="alias",
        ),
    ),
)
def test_command_directive(make_step, kwargs, expected_directive):
    step = make_step(**kwargs)
    assert step.directive.code == expected_directive
