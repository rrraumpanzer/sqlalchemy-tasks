from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import Movie
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, future=True)
session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
session = session_maker()


# BEGIN (write your solution here)

# END
