from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WarBase(BaseModel):
    war_number: int
    winner: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    shard: Optional[str] = None


class War(WarBase):
    id: int

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
