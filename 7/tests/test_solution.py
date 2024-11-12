import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from solution import delete_director
from models import Director, Movie, Base
import datetime
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
    director = Director(name="Christopher Nolan")
    movie1 = Movie(
        title="Inception",
        release_date=datetime.date(2010, 7, 16),
        duration=148,
        genre="Sci-Fi",
        rating=8.8,
        director=director,
    )
    movie2 = Movie(
        title="Interstellar",
        release_date=datetime.date(2014, 11, 7),
        duration=169,
        genre="Sci-Fi",
        rating=8.6,
        director=director,
    )
    session.add_all([director, movie1, movie2])
    session.commit()


@pytest.fixture
def session(engine, add_mock):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


def test_delete_director_with_movies(session):
    assert session.query(Director).count() == 1
    assert session.query(Movie).count() == 2

    director = session.query(Director).one()
    delete_director(session, director.id)

    assert session.query(Director).count() == 0
    assert session.query(Movie).count() == 0


def test_delete_non_existent_director(session):
    delete_director(session, 999)
    assert session.query(Director).count() == 0
    assert session.query(Movie).count() == 0
