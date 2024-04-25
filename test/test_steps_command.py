import inspect
from textwrap import dedent

import pytest


@pytest.mark.parametrize(
    "kwargs,expected_returncode,expected_output",
    (
        pytest.param(
            {"run": "echo hello"},
            0,
            dedent(
                """
                + echo hello
                hello

                """
            ).lstrip(),
            id="string",
        ),
        pytest.param(
            {"run": ["echo hello", "echo goodbye"]},
            0,
            dedent(
                """
                + echo hello
                hello

                + echo goodbye
                goodbye

                """
            ).lstrip(),
            id="list",
        ),
        pytest.param(
            {"run": "true && echo test"},
            0,
            dedent(
                """
                + true && echo test
                test

                """
            ).lstrip(),
            id="success && success",
        ),
        pytest.param(
            {"run": "false && echo test"},
            1,
            dedent(
                """
                + false && echo test

                """
            ).lstrip(),
            id="fail && success",
        ),
        pytest.param(
            {"run": "echo hello | cut -d'e' -f1"},
            0,
            dedent(
                """
                + echo hello | cut -d'e' -f1
                h

                """
            ).lstrip(),
            id="pipe",
        ),
    ),
)
def test_command_sync(make_step, capfd, kwargs, expected_returncode, expected_output):
    step = make_step(**kwargs)
    if inspect.isclass(expected_output) and issubclass(expected_output, Exception):
        with pytest.raises(expected_output):
            step.sync()
    else:
        assert step.sync() == expected_returncode
        out, err = capfd.readouterr()
        assert out == expected_output


@pytest.mark.parametrize(
    "kwargs,expected_directive",
    (
        pytest.param(
            {"run": "echo hello", "cwd": "workdir"},
            "echo hello in workdir",
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
    assert step.directive == expected_directive
