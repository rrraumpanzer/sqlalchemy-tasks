import datetime
from sqlalchemy import Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    movies: Mapped[list["Movie"]] = relationship("Movie", back_populates="director")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True)
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"), index=True)
    release_date: Mapped[datetime.date] = mapped_column(Date)
    duration: Mapped[int] = mapped_column(Integer)
    genre: Mapped[str] = mapped_column(String(32))
    rating: Mapped[float] = mapped_column(Float)
    director: Mapped[Director] = relationship("Director", back_populates="movies")
