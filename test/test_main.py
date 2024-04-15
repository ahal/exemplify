import pytest

from dittoed.installables.base import registry
from dittoed.main import generate_installables


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


@pytest.mark.parametrize("name", registry.keys())
def test_generate_installables_basic(name):
    step = {"type": name}
    step.update(defaults(name))
    config = {"meta": {"root": "cwd"}, name: {"step": [step]}}

    installables = list(generate_installables(config, [name]))
    assert len(installables) == 1
    assert isinstance(installables[0], registry[name])


@pytest.mark.parametrize(
    "config,routines,expected",
    (
        pytest.param({}, [], [], id="empty"),
        pytest.param({"foo": {"step": []}}, ["foo"], [], id="no step"),
    ),
)
def test_generate_installables_custom(config, routines, expected):
    installables = list(generate_installables(config, routines))
    assert len(installables) == len(expected)

    for i, installable in enumerate(installables):
        assert isinstance(installable, expected[i])
