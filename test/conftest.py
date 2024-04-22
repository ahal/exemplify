import pytest
from exemplify.steps.base import Step, registry


class FakeStep(Step):
    def __init__(self, meta: dict, key) -> None:
        self.key = key

    def sync(self, *args, **kwargs):
        pass


@pytest.fixture
def meta():
    return {}


@pytest.fixture
def make_step(request, meta):
    kind = request.module.__name__[len("test_steps_") :]

    def inner(*args, **kwargs):
        return registry[kind](meta, *args, **kwargs)

    return inner
