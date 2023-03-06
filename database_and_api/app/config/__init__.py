from sqlalchemy.exc import OperationalError
from common.db import get_engine
from config.logger import logger
from .create_app import create_app


app = create_app()


@app.on_event("startup")
async def startup_event():
    engine = get_engine()
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            logger.info("Database connection successful.")
    except OperationalError as err:
        logger.error(f"{err}")
