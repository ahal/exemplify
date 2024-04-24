import subprocess

import pytest

from exemplify.util import process


@pytest.mark.parametrize(
    "args, kwargs, expected_kwargs, expected_print",
    (
        pytest.param(
            (["echo", "foo"],),
            {},
            {
                "stdout": subprocess.PIPE,
                "stderr": subprocess.STDOUT,
                "text": True,
            },
            True,
            id="simple",
        ),
        pytest.param(
            (["echo", "foo"],),
            {"capture_output": True},
            {
                "text": True,
            },
            False,
            id="captured",
        ),
        pytest.param(
            (["echo", "foo"],),
            {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE},
            {
                "text": True,
            },
            False,
            id="captured",
        ),
        pytest.param(
            (["echo", "foo"],),
            {"stdout": subprocess.PIPE},
            {
                "stderr": subprocess.STDOUT,
                "text": True,
            },
            False,
            id="captured stdout only",
        ),
        pytest.param(
            (["echo", "foo"],),
            {"stderr": subprocess.PIPE},
            {
                "stdout": subprocess.PIPE,
                "text": True,
            },
            True,
            id="captured stderr only",
        ),
        pytest.param(
            (["echo", "foo"],),
            {"stdout": subprocess.DEVNULL},
            {
                "stderr": subprocess.STDOUT,
                "text": True,
            },
            False,
            id="devnull",
        ),
    ),
)
def test_run(mocker, args, kwargs, expected_kwargs, expected_print):
    mock_run = mocker.patch.object(process.subprocess, "run")
    mock_print = mocker.patch.object(process.console, "print")

    process.run(*args, **kwargs)

    kwargs.update(expected_kwargs)
    mock_run.assert_called_once_with(*args, **kwargs)
    assert mock_print.called == expected_print
