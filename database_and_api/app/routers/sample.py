from fastapi import APIRouter
from config.extensions import exception_handler as custom_exec
from config.logger import logger
from schemas.base import BaseListResponse
from schemas.sample import SampleResponse


router = APIRouter()


@router.get("/hello_world", response_model=BaseListResponse[SampleResponse])
def hello_world():
    return {"data": [{"test": "test"}], "total": 0}


@router.get("/raise_error")
def raise_error():
    logger.error("Bad Request")
    raise custom_exec.BadRequest(400000, "Bad Request")
