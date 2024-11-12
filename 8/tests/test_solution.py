import pytest
import pytest_asyncio
import datetime
from models import Director, Movie
from solution import get_all_movies

@pytest_asyncio.fixture
async def mock_director():
    return Director(name="Frank Darabont")

@pytest_asyncio.fixture
async def mock_movies(mock_director):
    return [
        Movie(
            title="The Shawshank Redemption",
            release_date=datetime.date(1994, 9, 23),
            duration=142,
            genre="Drama",
            rating=9.3,
            director=mock_director,
        ),
        Movie(
            title="The Green Mile",
            release_date=datetime.date(1999, 12, 10),
            duration=189,
            genre="Drama",
            rating=8.6,
            director=mock_director,
        ),
    ]

@pytest_asyncio.fixture
async def add_mock_data(async_session, mock_director, mock_movies):
    async with async_session.begin():
        async_session.add(mock_director)
        async_session.add_all(mock_movies)

@pytest.mark.asyncio
async def test_get_all_movies(async_session, add_mock_data):
    expected_movies = [
        "The Shawshank Redemption by Frank Darabont, released on 1994-09-23, duration: 142 min, genre: Drama, rating: 9.3",
        "The Green Mile by Frank Darabont, released on 1999-12-10, duration: 189 min, genre: Drama, rating: 8.6"
    ]
    
    movies = await get_all_movies(async_session)
    
    assert len(movies) == 2
    assert all(expected_movie in movies for expected_movie in expected_movies)