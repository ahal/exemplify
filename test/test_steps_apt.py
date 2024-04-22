import inspect
import subprocess

import pytest

from exemplify.steps import distro


@pytest.mark.parametrize(
    "kwargs,expected",
    (
        pytest.param(
            {"packages": "foo"},
            [
                (
                    (["dpkg", "-s", "foo"],),
                    {"stdout": subprocess.DEVNULL, "stderr": subprocess.STDOUT},
                ),
                ((["sudo", "apt", "upgrade", "-y", "foo"],),),
            ],
            id="string",
        ),
        pytest.param(
            {"packages": ["foo", "bar"]},
            [
                (
                    (["dpkg", "-s", "foo"],),
                    {"stdout": subprocess.DEVNULL, "stderr": subprocess.STDOUT},
                ),
                (
                    (["dpkg", "-s", "bar"],),
                    {"stdout": subprocess.DEVNULL, "stderr": subprocess.STDOUT},
                ),
                ((["sudo", "apt", "upgrade", "-y", "foo", "bar"],),),
            ],
            id="list",
        ),
    ),
)
def test_apt_sync(make_step, mocker, kwargs, expected):
    m = mocker.patch.object(distro.subprocess, "check_call")

    ins = make_step(**kwargs)
    if inspect.isclass(expected) and issubclass(expected, Exception):
        with pytest.raises(expected):
            ins.sync()
    else:
        ins.sync()
        assert m.call_args_list == expected
