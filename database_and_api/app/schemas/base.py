from typing import Any, List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseObjectResponse(BaseModel):
    pass


class BaseListResponse(BaseModel, Generic[T]):
    total: int
    data: List[T]


class BaseORMResponse(BaseModel):
    class Config:
        orm_mode = True
        # allow_population_by_field_name = True
