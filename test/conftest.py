from pathlib import Path
import pytest

from exemplify.main import exemplify
from exemplify.steps.base import Step, registry

here = Path(__file__).parent


class FakeStep(Step):
    name = "fake"

    def __init__(self, meta: dict, key) -> None:
        self.key = key

    @property
    def directive(self):
        return "run fake"

    def sync(self, *args, **kwargs) -> int:
        return 0


@pytest.fixture
def meta():
    return {}


@pytest.fixture
def make_step(request, meta):
    kind = request.module.__name__[len("test_steps_") :]

    def inner(*args, **kwargs):
        return registry[kind](meta, *args, **kwargs)

    return inner


@pytest.fixture
def run_exemplify(capfd, tmp_path):
    def inner(exemplify_toml, verbose=False):
        config_path = tmp_path / "exemplify.toml"
        config_path.write_text(exemplify_toml)

        ret = exemplify(tmp_path, verbose=verbose)

        out, err = capfd.readouterr()
        if out:
            print(f"Captured stdout:\n{out}")
        if err:
            print(f"Captured stderr:\n{err}")

        return ret, out, err

    return inner
