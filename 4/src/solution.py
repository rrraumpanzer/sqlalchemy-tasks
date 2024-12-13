from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie
import os
from dotenv import load_dotenv


load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"])

session = sessionmaker(bind=engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# BEGIN (write your solution here)
def format_movie(movie):
    return (
        f"{movie.title} by {movie.director}, released on {movie.release_date}, "
        f"duration: {movie.duration} min, genre: {movie.genre}, rating: {movie.rating}"
    )

def get_all_movies(session):
    stmt = select(Movie)
    return [format_movie(movie) for movie in session.scalars(stmt)]

def get_movies_by_director(session, director_name):
    stmt = (
        select(Movie)
        .filter(Movie.director == director_name)
        .order_by(Movie.release_date)
    )
    return [format_movie(movie) for movie in session.scalars(stmt)]

def get_top_rated_movies(session, n):
    stmt = select(Movie).order_by(Movie.rating.desc()).limit(n)
    return [format_movie(movie) for movie in session.scalars(stmt)]
# END
