import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from solution import Base, Book, add_books
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


@pytest.fixture
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_add_books(engine, session):
    add_books(engine)
    books = session.query(Book).all()
    assert len(books) == 2
    assert books[0].title == "To Kill a Mockingbird"
    assert books[0].author == "Harper Lee"
    assert books[0].published_year == 1960
    assert books[1].title == "1984"
    assert books[1].author == "George Orwell"
    assert books[1].published_year == 1949
