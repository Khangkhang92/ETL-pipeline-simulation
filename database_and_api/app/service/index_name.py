from models import IndexName
from .base_service import BaseService
from sqlalchemy.orm import Session
from sqlalchemy import select


class IndexNameService(BaseService):
    def fetch_index_name(self, ticker, session: Session):
        stmt = select(IndexName).where(IndexName.index_id == ticker.upper())
        return session.execute(stmt).scalar_one()


index_name_service = IndexNameService()
