import inspect
import subprocess
from textwrap import dedent

import pytest


@pytest.mark.parametrize(
    "kwargs,expected",
    (
        pytest.param(
            {"run": "echo hello"},
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
            dedent(
                """
                + true
                + echo test
                test
                """
            ).lstrip(),
            id="success && success",
        ),
        pytest.param(
            {"run": "false && echo test"},
            subprocess.CalledProcessError,
            id="fail && success",
        ),
        pytest.param(
            {"run": "echo hello | cut -d'e' -f1"},
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
def test_command_sync(make_installable, capfd, kwargs, expected):
    ins = make_installable(**kwargs)
    if inspect.isclass(expected) and issubclass(expected, Exception):
        with pytest.raises(expected):
            ins.sync()
    else:
        ins.sync()
        out, err = capfd.readouterr()
        assert out == expected
