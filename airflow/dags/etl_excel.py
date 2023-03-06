from datetime import datetime, timedelta
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
from functools import lru_cache
from typing import Optional, Dict, Any
from pydantic import BaseSettings, validator, PostgresDsn
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import MetaData, Table
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import time
import tracemalloc
from loguru import logger


def time_benchmark(func):
    """
    Logging how much time a function takes
    """

    def profile(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        excercute_time = round(end - start, 3)
        logger.info(f"Function {func.__name__} takes {excercute_time} s")
        return res

    profile.__name__ = func.__name__
    return profile


def memory_benchmark(func):
    """
    Logging how much memory a function takes
    """

    def profile(*args, **kwargs):
        tracemalloc.start()
        res = func(*args, **kwargs)
        cur, peak = tracemalloc.get_traced_memory()
        logger.info(
            f"Function {func.__name__} takes {cur} byte now in memory "
            f"and peak size in memory is {peak} byte"
        )
        tracemalloc.stop()
        return res

    profile.__name__ = func.__name__
    return profile


class Settings(BaseSettings):

    # App configuration
    SECRET_KEY: str = ""
    TIMEFRAME: str = "H"
    EXCEL_PATH: str

    # Database configuration
    INSERT_CHUNK_SIZE: int = None
    DB_HOST: str
    DB_PORT: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, allow_reuse=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        sqlalchemy_uri = PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USERNAME"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_NAME') or ''}",
            port=values.get("DB_PORT"),
        )
        os.environ["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_uri
        return sqlalchemy_uri

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


def get_engine():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        poolclass=NullPool,
        executemany_mode="values",
        executemany_values_page_size=10000,
        executemany_batch_page_size=50000,
    )
    print(settings.SQLALCHEMY_DATABASE_URI)
    return engine


engine = get_engine()


def _create_upsert_method(engine: object):
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


def _save_todb(table_name: str, df: pd.DataFrame, upsert: bool = False) -> None:
    engine = get_engine()
    upsert_method = _create_upsert_method(engine) if upsert else None
    df.to_sql(
        table_name,
        con=engine,
        index=False,
        if_exists="append",
        chunksize=settings.INSERT_CHUNK_SIZE,
        method=upsert_method,
    )
    logger.info(f"saving data to {table_name} is complete")


def _check_connection() -> None:
    with engine.connect() as connection:
        connection.execute("SELECT 1")
        logger.info("Database connection successful")


@time_benchmark
def _pre_read_excel(path: str) -> pd.DataFrame:

    expected_column_names = [
        "indexId",
        "chartOpen",
        "chartHigh",
        "chartLow",
        "chartClose",
        "totalQtty",
        "totalValue",
        "dateTime",
        "date",
        "time",
    ]
    if not os.path.exists(path):
        logger.error(f"File or directory {path} does not exist")

    etf = pd.read_excel(path, sheet_name=0, nrows=1, usecols=expected_column_names)
    return etf


def excel_to_pickel() -> None:
    cwd = os.getcwd()
    path = os.path.join(cwd, settings.EXCEL_PATH)
    _pre_read_excel(path)
    etf = pd.read_excel(path, sheet_name=0)
    etf.to_pickle(os.path.join(cwd, "tmp/frame_m1.pkl"))
    logger.info("reading excel file is complete!")


def change_time_frame() -> None:

    etf = pd.read_pickle(os.path.join(os.getcwd(), "tmp/frame_m1.pkl"))

    ohlc = {
        "chartOpen": "first",
        "chartHigh": "max",
        "chartLow": "min",
        "chartClose": "last",
        "totalQtty": "sum",
        "totalValue": "sum",
    }
    df = (
        etf.set_index(pd.DatetimeIndex(etf["dateTime"]))
        .groupby("indexId")
        .resample(settings.TIMEFRAME)
        .apply(ohlc)
    )
    df = df.drop(df[df.chartOpen.isnull()].index).reset_index()
    df["time"] = pd.to_datetime(df["dateTime"]).dt.time
    df["date"] = pd.to_datetime(df["dateTime"]).dt.date
    df.to_pickle(os.path.join(os.getcwd(), "tmp/frame_h1.pkl"))
    logger.info("change timeframe and save to pickle file are complete!")


@time_benchmark
def _save_index_name() -> None:
    df = pd.read_pickle(os.path.join(os.getcwd(), "tmp/frame_h1.pkl"))
    list_index = df["indexId"].unique().tolist()
    ds = pd.DataFrame({"index_id": list_index})
    _save_todb("index_name", ds, upsert=True)
    _save_todb("index_frame_h1", df, upsert=True)


@time_benchmark
def _save_frame_m1() -> None:
    df = pd.read_pickle(os.path.join(os.getcwd(), "tmp/frame_m1.pkl"))
    _save_todb("index_frame_m1", df, upsert=True)


def save_data() -> None:
    _check_connection()
    _save_index_name()
    _save_frame_m1()


with DAG(
    dag_id="etl_excel",
    description="load excel data to database",
    start_date=airflow.utils.dates.days_ago(50),
    schedule_interval="*/5 * * * *",  # at every  5  minute
    is_paused_upon_creation=True,
    max_active_tasks=10,
    max_active_runs=10,
    dagrun_timeout=timedelta(hours=1),
    default_view="grid",
    catchup=False,
) as dag:

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=excel_to_pickel,
        op_kwargs={
            "to_time": "{{ data_interval_end.strftime('%Y-%m-%d') }}",
        },
    )
    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=change_time_frame,
        op_kwargs={
            "to_time": "{{ data_interval_end.strftime('%Y-%m-%d') }}",
        },
    )
    load_data_2_postgresql = PythonOperator(
        task_id="execel_2_db",
        python_callable=save_data,
        op_kwargs={
            "to_time": "{{ data_interval_end.strftime('%Y-%m-%d') }}",
        },
    )

    # data pipeline
    extract_data >> transform_data >> load_data_2_postgresql
