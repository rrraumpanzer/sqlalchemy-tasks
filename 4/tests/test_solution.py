import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from solution import get_all_movies, get_movies_by_director, get_top_rated_movies
from models import Base, Movie
from datetime import date
import os
from dotenv import load_dotenv

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
    movies = [
        Movie(
            id=1,
            title="The Shawshank Redemption",
            director="Frank Darabont",
            release_date=date(1994, 9, 23),
            duration=142,
            genre="Drama",
            rating=9.3,
        ),
        Movie(
            id=2,
            title="The Godfather",
            director="Francis Ford Coppola",
            release_date=date(1972, 3, 24),
            duration=175,
            genre="Crime",
            rating=9.2,
        ),
        Movie(
            id=3,
            title="Gladiator",
            director="Ridley Scott",
            release_date=date(2000, 5, 5),
            duration=155,
            genre="Action",
            rating=8.5,
        ),
        Movie(
            id=4,
            title="Alien",
            director="Ridley Scott",
            release_date=date(1979, 5, 25),
            duration=117,
            genre="Horror",
            rating=8.4,
        ),
    ]
    session.add_all(movies)
    session.commit()
    session.close()


@pytest.fixture
def session(engine, add_mock):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()  # Rollback any changes made during the test
    session.close()


def test_get_all_movies(session):
    movies = get_all_movies(session)
    assert len(movies) == 4
    assert (
        movies[0]
        == "The Shawshank Redemption by Frank Darabont, released on 1994-09-23, duration: 142 min, genre: Drama, rating: 9.3"
    )


def test_get_movies_by_director(session):
    movies = get_movies_by_director(session, "Ridley Scott")
    assert len(movies) == 2
    assert (
        movies[0]
        == "Alien by Ridley Scott, released on 1979-05-25, duration: 117 min, genre: Horror, rating: 8.4"
    )
    assert (
        movies[1]
        == "Gladiator by Ridley Scott, released on 2000-05-05, duration: 155 min, genre: Action, rating: 8.5"
    )


def test_get_top_rated_movies(session):
    movies = get_top_rated_movies(session, 2)
    assert len(movies) == 2
    assert (
        movies[0]
        == "The Shawshank Redemption by Frank Darabont, released on 1994-09-23, duration: 142 min, genre: Drama, rating: 9.3"
    )
    assert (
        movies[1]
        == "The Godfather by Francis Ford Coppola, released on 1972-03-24, duration: 175 min, genre: Crime, rating: 9.2"
    )
