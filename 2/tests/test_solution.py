import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from solution import Base, Book
import os
from dotenv import load_dotenv
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


@pytest.fixture
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_book_field_types(session):
    new_book = Book(
        title="Test Book",
        author="Test Author",
        published_date=datetime.date(2021, 1, 1),
        pages=100,
        genre="Fiction",
        rating=4.5,
    )
    session.add(new_book)
    session.commit()

    book_from_db = session.query(Book).filter_by(title="Test Book").first()

    # Проверка типов полей
    assert isinstance(book_from_db.id, int)
    assert isinstance(book_from_db.title, str)
    assert isinstance(book_from_db.author, str)
    assert isinstance(book_from_db.published_date, datetime.date)
    assert isinstance(book_from_db.pages, int)
    assert isinstance(book_from_db.genre, str)
    assert isinstance(book_from_db.rating, float)


def test_book_constraints(session):
    # Проверка уникальности заголовка
    book1 = Book(
        title="Unique Title",
        author="Author One",
        published_date=datetime.date(2020, 1, 1),
        pages=200,
        genre="Non-Fiction",
        rating=4.0,
    )
    session.add(book1)
    session.commit()

    book2 = Book(
        title="Unique Title",  # Дублирующий заголовок
        author="Author Two",
        published_date=datetime.date(2021, 1, 1),
        pages=150,
        genre="Fiction",
        rating=4.5,
    )
    session.add(book2)

    with pytest.raises(Exception):  # Ожидаем исключение при нарушении уникальности
        session.commit()
