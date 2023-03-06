from .base import BaseORMResponse
from datetime import time, date, datetime
from typing import List, Optional


class IndexFrameM1Response(BaseORMResponse):
    id: Optional[int]
    indexId: Optional[str]
    chartOpen: Optional[float]
    chartLow: Optional[float]
    chartHigh: Optional[float]
    chartClose: Optional[float]
    totalQtty: Optional[float]
    totalValue: Optional[float]

    valueMA30: Optional[int]
    valueMA14: Optional[int]
    valueMA7: Optional[int]
    time: Optional[time]
    date: Optional[date]
    dateTime: Optional[datetime]
