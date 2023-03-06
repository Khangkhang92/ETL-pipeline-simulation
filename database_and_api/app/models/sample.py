from sqlalchemy import Column, String
from .base import CommonModel


class SampleModel(CommonModel):
    name = Column(String(length=50))
