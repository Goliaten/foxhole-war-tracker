from typing import Optional
from pydantic import BaseModel


class Shard(BaseModel):
    id: int
    REV: int
    url: str
    name: Optional[str]

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
