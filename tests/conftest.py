import pytest
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope="module")
def test_db():
    initializer(["app.models"], db_url="sqlite://:memory:")
    yield
    finalizer()
