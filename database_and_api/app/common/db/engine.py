from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from config.settings import settings


def get_engine():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        poolclass=NullPool,
        executemany_mode="values",
        executemany_values_page_size=10000,
        executemany_batch_page_size=50000,
    )
    return engine
