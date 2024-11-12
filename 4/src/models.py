from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Movie(title='{self.title}', director='{self.director}', release_date='{self.release_date}')>"
