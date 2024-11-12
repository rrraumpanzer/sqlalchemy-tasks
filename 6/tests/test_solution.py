import pytest
from solution import get_movies_with_directors
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Director, Movie
from dotenv import load_dotenv
import os
import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine

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

    director1 = Director(name="Frank Darabont")
    director2 = Director(name="Christopher Nolan")

    movie1 = Movie(
        title="The Shawshank Redemption",
        release_date=datetime.date(1994, 9, 23),
        duration=142,
        genre="Drama",
        rating=9.3,
        director=director1,
    )
    movie2 = Movie(
        title="Inception",
        release_date=datetime.date(2010, 7, 16),
        duration=148,
        genre="Sci-Fi",
        rating=8.8,
        director=director2,
    )

    session.add_all([director1, director2, movie1, movie2])
    session.commit()


@pytest.fixture
def session(engine, add_mock):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


def test_get_movies_with_directors(session):
    query_count = [0]

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        query_count[0] += 1

    result = get_movies_with_directors(session)

    # expected = [
    #     "Inception by Christopher Nolan, released on 2010-07-16, duration: 148 min, genre: Sci-Fi, rating: 8.8",
    #     "The Shawshank Redemption by Frank Darabont, released on 1994-09-23, duration: 142 min, genre: Drama, rating: 9.3"
    # ]
    # assert result == expected

    assert query_count[0] == 1  # Проверка, что выполнен только один запрос
    assert result[0].director is not None
