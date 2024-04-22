import pytest
from dittoed.installables.base import Installable, registry


class FakeInstallable(Installable):
    def __init__(self, meta: dict, key) -> None:
        self.key = key

    def sync(self, *args, **kwargs):
        pass


@pytest.fixture
def meta():
    return {}


@pytest.fixture
def make_installable(request, meta):
    kind = request.module.__name__[len("test_installables_") :]

    def inner(*args, **kwargs):
        return registry[kind](meta, *args, **kwargs)

    return inner


