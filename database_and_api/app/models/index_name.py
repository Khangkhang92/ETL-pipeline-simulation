from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import CommonModel


class IndexName(CommonModel):

    __tablename__ = "index_name"
    index_id = Column(String, unique=True)

    frame_h1 = relationship(
        "IndexFrameH1",
        back_populates="stock_name",
        order_by="desc(IndexFrameH1.dateTime)",
    )

    frame_m1 = relationship(
        "IndexFrameM1",
        back_populates="stock_name",
        order_by="desc(IndexFrameM1.dateTime)",
    )
