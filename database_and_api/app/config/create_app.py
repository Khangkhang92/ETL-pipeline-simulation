from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
from .extensions.exception_handler import APIException, api_error_handler
from .settings import get_settings


settings = get_settings()


def create_app():
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_PREFIX_URL}/openapi.json",
        docs_url=f"{settings.API_PREFIX_URL}/docs",
        redoc_url=f"{settings.API_PREFIX_URL}/redoc",
    )
    configure_app(app)
    return app


def configure_app(app: FastAPI):
    configure_logging_handler(app)
    configure_exception_handler(app)
    configure_middleware(app)
    configure_router(app)


def configure_logging_handler(app: FastAPI):
    pass


def configure_exception_handler(app: FastAPI):
    app.add_exception_handler(APIException, api_error_handler)


def configure_router(app: FastAPI):
    app.include_router(router, prefix=settings.API_PREFIX_URL)


def configure_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = create_app()
