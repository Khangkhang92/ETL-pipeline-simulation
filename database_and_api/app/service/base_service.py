from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import MetaData, Table
import pandas as pd
from common.db import get_engine
from config.logger import logger
from config.settings import settings


class BaseService:
    def _create_upsert_method(self, engine: object):
        def method(table, conn, keys, data_iter):

            meta = MetaData(engine)
            sql_table = Table(table.name, meta, autoload=True)
            values_to_insert = [dict(zip(keys, data)) for data in data_iter]
            insert_stmt = insert(sql_table, values_to_insert)
            update_stmt = {exc_k.key: exc_k for exc_k in insert_stmt.excluded}
            upsert_stmt = insert_stmt.on_conflict_do_update(
                constraint=sql_table._sorted_constraints.pop().name,
                set_=update_stmt,
            )
            conn.execute(upsert_stmt)

        return method

    def _save_todb(
        self, table_name: str, df: pd.DataFrame, upsert: bool = False
    ) -> None:
        engine = get_engine()
        upsert_method = self._create_upsert_method(engine) if upsert else None
        df.to_sql(
            table_name,
            con=engine,
            index=False,
            if_exists="append",
            chunksize=settings.INSERT_CHUNK_SIZE,
            method=upsert_method,
        )
        logger.info(f"saving data to {table_name} is complete")


baseservice = BaseService()
