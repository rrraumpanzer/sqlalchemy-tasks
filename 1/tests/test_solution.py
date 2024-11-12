import os
import pytest
from sqlalchemy.exc import OperationalError
from solution import create_db_engine


@pytest.fixture(scope="module")
def db_url():
    url = os.getenv("DATABASE_URL")
    assert url is not None, "DATABASE_URL must be set"
    return url


def test_engine_connection(db_url):
    engine = create_db_engine(db_url)
    try:
        with engine.connect() as connection:
            assert not connection.closed
    except OperationalError:
        pytest.fail("Не удалось подключиться к базе данных")
    assert connection.closed
