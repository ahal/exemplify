import pytest


@pytest.fixture
def config():
    return {"meta": {"defaults": ["foo", "bar"]}}
