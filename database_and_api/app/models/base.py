from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CommonModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
