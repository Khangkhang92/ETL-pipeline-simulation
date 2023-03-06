from sqlalchemy import (
    Column,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    Float,
    BigInteger,
    Date,
    Time,
    String,
)
from sqlalchemy.orm import relationship
from .base import CommonModel


class IndexFrameM1(CommonModel):

    __tablename__ = "index_frame_m1"

    indexId = Column(String, ForeignKey("index_name.index_id"))
    chartOpen = Column(Float)
    chartLow = Column(Float)
    chartHigh = Column(Float)
    chartClose = Column(Float)
    totalQtty = Column(BigInteger)
    totalValue = Column(BigInteger)
    valueMA30 = Column(BigInteger)
    valueMA14 = Column(BigInteger)
    valueMA7 = Column(BigInteger)
    date = Column(Date)
    time = Column(Time)
    dateTime = Column(DateTime)

    stock_name = relationship("IndexName", back_populates="frame_m1")

    __table_args__ = (UniqueConstraint("indexId", "dateTime", name="m1_upsert_key_un"),)
