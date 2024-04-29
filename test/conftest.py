from pathlib import Path
import pytest
from exemplify.steps.base import Step, registry

here = Path(__file__).parent


@pytest.fixture(scope="session")
def datadir():
    return here / "data"


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
