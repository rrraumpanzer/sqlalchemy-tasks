import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Date, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"])


# BEGIN (write your solution here)

# END

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
