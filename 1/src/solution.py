import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


# BEGIN (write your solution here)
def create_db_engine(db_url=None, echo=False, pool_size=5, max_overflow=10):
    db_url = db_url or os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set or provided.")
    return create_engine(
        db_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow
    )
# END
