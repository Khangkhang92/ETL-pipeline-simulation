from fastapi import APIRouter, Depends
from service import handle_data, index_name_service
from common.db.session import ScopedSession
from schemas import IndexNameResponse


router = APIRouter()


@router.get("/simulation_fetch_data", response_model=IndexNameResponse)
async def fetch_data(ticker: str, session: ScopedSession = Depends(ScopedSession)):
    return index_name_service.fetch_index_name(ticker, session)


@router.post("/etl_data")
async def manual_etl():
    handle_data.manual_etl_data()
    return {"etl_data manually is complet!"}
