from .base import BaseORMResponse
from typing import List
from datetime import time, date, datetime
from typing import List, Optional


class IndexFrameH1Response(BaseORMResponse):
    id: Optional[int]
    indexId: Optional[str]
    chartOpen: Optional[float]
    chartLow: Optional[float]
    chartHigh: Optional[float]
    chartClose: Optional[float]
    totalQtty: Optional[float]
    totalValue: Optional[float]
    date: Optional[date]
    time: Optional[time]
    dateTime: Optional[datetime]
