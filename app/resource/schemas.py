from datetime import datetime

from pydantic import BaseModel


class ResourceBase(BaseModel):
    name: str


class ResourceInput(ResourceBase):
    pass


class Resource(ResourceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ResourceFilters(BaseModel):
    created_at_gte: datetime | None
    created_at_lte: datetime | None
