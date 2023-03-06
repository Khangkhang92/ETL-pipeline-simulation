from fastapi import APIRouter
from .etl_excel import router as etl_router

router = APIRouter()
router.include_router(etl_router, prefix="/etf_data", tags=["ETL_data"])
