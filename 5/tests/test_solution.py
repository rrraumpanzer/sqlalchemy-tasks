import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from solution import get_movies_with_directors
from models import Base, Director, Movie
from dotenv import load_dotenv
import os
import datetime

load_dotenv()


@pytest.fixture(scope="module")
def engine():
    return create_engine(os.environ["DATABASE_URL"])


@pytest.fixture(scope="module")
def tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def add_mock(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()

    director = Director(name="Frank Darabont")
    movie = Movie(
        title="The Shawshank Redemption",
        release_date=datetime.date(1994, 9, 23),
        duration=142,
        genre="Drama",
        rating=9.3,
        director=director,
    )

    session.add(director)
    session.add(movie)
    session.commit()


@pytest.fixture
def session(engine, add_mock):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


def test_get_movies_with_directors(session):
    result = get_movies_with_directors(session)
    expected = [
        "The Shawshank Redemption by Frank Darabont, released on 1994-09-23, duration: 142 min, genre: Drama, rating: 9.3"
    ]

    assert result == expected
