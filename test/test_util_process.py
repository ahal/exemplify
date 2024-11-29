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
    mock_stdout = mocker.PropertyMock()
    mock_stdout.readline.side_effect = ["foobar", None]

    mock_proc = mocker.MagicMock(new_callable=mocker.PropertyMock)
    mock_proc.stdout = mock_stdout

    mock_popen = mocker.patch.object(process.subprocess, "Popen", return_value=mock_proc)

    mock_print = mocker.patch.object(process.console, "print")

    process.run(*args, **kwargs)

    kwargs.update(expected_kwargs)
    mock_popen.assert_called_once_with(*args, **kwargs)
    assert mock_print.called == expected_print
