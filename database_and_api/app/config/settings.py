import os
from functools import lru_cache
from typing import Optional, Dict, Union, List, Any
from pydantic import BaseSettings, validator, PostgresDsn


class Settings(BaseSettings):

    # App configuration
    APP_NAME: str = "6P"
    BACKEND_CORS_ORIGIN: Union[List[str], str] = ["*"]
    API_PREFIX_URL: str = "/api/v1"
    APP_SECRET_KEY: str = ""
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

    @validator("BACKEND_CORS_ORIGIN", pre=True, allow_reuse=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            if v.startswith("["):
                v = v[1 : len(v) - 1]
            if v.endswith("]"):
                v = v[: len(v) - 2]
            return [i.strip().replace('"', "").replace("'", "") for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    LOG_INFO_FILE: str = "logs/info/infos.log"
    LOG_ERROR_FILE: str = "logs/error/errors.log"
    LOG_CUSTOM_FILE: str = "logs/custom/customs.log"
    LOG_SQL_FILE: str = "logs/sql/sql.log"
    LOG_ROTATION: str = "1 days"
    LOG_RETENTION: str = "20 days"
    LOG_FORMAT: str = (
        "[<level>{level}</level>] | "
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS} </green> | "
        "<cyan>{name}</cyan>:<cyan>{module}</cyan> | "
        "{line} | "
        "<level>{message}</level>"
    )

    LOG_DIAGNOSE: bool = True
    SQL_ECHO: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
