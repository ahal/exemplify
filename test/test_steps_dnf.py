import inspect

import pytest

from exemplify.steps.package.distro import dnf


@pytest.mark.parametrize(
    "kwargs,expected",
    (
        pytest.param(
            {"packages": "foo"},
            [
                ((["dnf", "list", "--installed", "foo"],),),
                ((["sudo", "dnf", "upgrade", "-y", "foo"],),),
            ],
            id="string",
        ),
        pytest.param(
            {"packages": ["foo", "bar"]},
            [
                ((["dnf", "list", "--installed", "foo"],),),
                ((["dnf", "list", "--installed", "bar"],),),
                ((["sudo", "dnf", "upgrade", "-y", "foo", "bar"],),),
            ],
            id="list",
        ),
    ),
)
def test_dnf_sync(make_step, mocker, kwargs, expected):
    m = mocker.patch.object(dnf, "run")

    ins = make_step(**kwargs)
    if inspect.isclass(expected) and issubclass(expected, Exception):
        with pytest.raises(expected):
            ins.sync()
    else:
        ins.sync()
        assert m.call_args_list == expected
