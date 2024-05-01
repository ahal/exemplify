import traceback
from pprint import pprint
from textwrap import dedent

import pytest

from exemplify import main

from conftest import FakeStep


@pytest.mark.parametrize(
    "config, expected",
    (
        pytest.param(
            "",
            {"meta": {"root": ""}},
            id="empty",
        ),
        pytest.param(
            dedent(
                """
        [[foo.step]]
        type = "command"
        run = "echo hello"
        """
            ),
            {
                "foo": {"step": [{"type": "command", "run": "echo hello"}]},
                "meta": {"root": ""},
            },
            id="basic",
        ),
    ),
)
def test_parse_config(mocker, config, expected):
    m = mocker.patch("builtins.open", mocker.mock_open(read_data=config))

    result = main.parse_config("path")
    m.assert_called_once_with("path", "rb")
    assert result == expected


def test_parse_config_include(mocker):
    mock1 = mocker.MagicMock()
    mock1.read.return_value = b"""
    [meta]
    include = ["other"]

    [[foo.step]]
    type = "foo"
    """

    mock2 = mocker.MagicMock()
    mock2.read.return_value = b"""
    [[bar.step]]
    type = "bar"
    """

    open_mock = mocker.mock_open()
    open_mock.return_value.__enter__.side_effect = [mock1, mock2]

    mocker.patch("builtins.open", open_mock)

    result = main.parse_config("exemplify.toml")
    print("Dump for copy/paste:")
    pprint(result, indent=2)
    assert result == {
        "bar": {"step": [{"type": "bar"}]},
        "foo": {"step": [{"type": "foo"}]},
        "meta": {"root": ""},
    }


def defaults(_type):
    if _type == "command":
        return {"run": "echo hello"}
    if _type == "link":
        return {"source": "foo"}
    if _type in ("apt", "cargo", "dnf", "npm", "pip"):
        return {"packages": "foo"}
    if _type in ("pipx",):
        return {"package": "foo"}
    if _type in ("hg", "git"):
        return {"repo": "https://example.com/repo", "dest": "bar"}
    return {}


@pytest.mark.parametrize("name", main.registry.keys())
def test_generate_steps_basic(name):
    step = {"type": name}
    step.update(defaults(name))
    config = {"meta": {"root": "cwd"}, name: {"step": [step]}}

    steps = list(main.generate_steps(name, config))
    assert len(steps) == 1
    assert isinstance(steps[0], main.registry[name])


def assert_empty(e):
    assert isinstance(e, KeyError)


def assert_no_step(steps):
    assert steps == []


def assert_interpolate(steps):
    assert len(steps) == 1
    ins = steps[0]
    assert isinstance(ins, FakeStep)
    assert ins.key == "some thing"


@pytest.mark.parametrize(
    "routine,config",
    (
        pytest.param("", {}, id="empty"),
        pytest.param("foo", {"foo": {"step": []}}, id="no_step"),
        pytest.param(
            "foo",
            {
                "foo": {
                    "meta": {"value": "thing"},
                    "step": [{"type": "foo", "key": "some {value}"}],
                },
            },
            id="interpolate",
        ),
    ),
)
def test_generate_steps_custom(request, mocker, routine, config):
    mocker.patch.dict(main.registry, {"foo": FakeStep, "bar": FakeStep})

    try:
        result = list(main.generate_steps(routine, config))
    except Exception as e:
        traceback.print_exc()
        result = e

    param_id = request.node.callspec.id
    assert_func = globals()[f"assert_{param_id}"]
    assert_func(result)
