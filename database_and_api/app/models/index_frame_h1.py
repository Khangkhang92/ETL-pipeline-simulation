from sqlalchemy import (
    Column,
    ForeignKey,
    UniqueConstraint,
    String,
    DateTime,
    Float,
    BigInteger,
    Date,
    Time,
)
from sqlalchemy.orm import relationship
from .base import CommonModel


class IndexFrameH1(CommonModel):

    __tablename__ = "index_frame_h1"

    indexId = Column(String, ForeignKey("index_name.index_id"))
    chartOpen = Column(Float)
    chartLow = Column(Float)
    chartHigh = Column(Float)
    chartClose = Column(Float)
    totalQtty = Column(BigInteger)
    totalValue = Column(BigInteger)
    date = Column(Date)
    time = Column(Time)
    dateTime = Column(DateTime)

    stock_name = relationship("IndexName", back_populates="frame_h1")

    __table_args__ = (UniqueConstraint("indexId", "dateTime", name="h1_upsert_key_un"),)
