# Custom Logger Using Loguru

import logging
import sys

from loguru import logger

from .settings import settings


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class Loguru:
    @classmethod
    def customize_logging(cls):
        # Remove default logging
        logger.remove()
        # Add an custom level
        logger.level("CUSTOM", no=41, color="<magenta>")

        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=False,
            level="INFO",
            diagnose=settings.LOG_DIAGNOSE,
            format=settings.LOG_FORMAT,
        )

        # Get only INFO logs
        logger.add(
            settings.LOG_INFO_FILE,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            enqueue=True,
            diagnose=settings.LOG_DIAGNOSE,
            backtrace=True,
            level="INFO",
            format=settings.LOG_FORMAT,
            filter=lambda record: record["level"].name == "INFO",
        )

        # Get ERROR logs
        logger.add(
            settings.LOG_ERROR_FILE,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            enqueue=True,
            diagnose=settings.LOG_DIAGNOSE,
            backtrace=True,
            level="ERROR",
            format=settings.LOG_FORMAT,
            filter=lambda record: record["level"].name == "ERROR",
        )

        # Get CUSTOM logs
        logger.add(
            settings.LOG_CUSTOM_FILE,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            enqueue=True,
            diagnose=settings.LOG_DIAGNOSE,
            backtrace=True,
            level="CUSTOM",
            format=settings.LOG_FORMAT,
        )

        logging.basicConfig(handlers=[InterceptHandler()])
        if settings.SQL_ECHO:
            logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
            logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)
            # Get SQL logs
            logger.add(
                settings.LOG_SQL_FILE,
                rotation=settings.LOG_ROTATION,
                retention=settings.LOG_RETENTION,
                enqueue=True,
                diagnose=settings.LOG_DIAGNOSE,
                backtrace=True,
                level="INFO",
                format=settings.LOG_FORMAT,
                filter="sqlalchemy.engine",
            )
        return logger.bind(request_id=None, method=None)


custom_log = Loguru()
logger = custom_log.customize_logging()
