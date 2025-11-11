from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WarState(BaseModel):
    id: int
    REV: int
    shard_id: int
    warId: Optional[str]
    warNumber: int
    winner: Optional[str]
    conquestStartTime: datetime
    conquestEndTime: Optional[datetime]
    resistanceStartTime: Optional[datetime]
    scheduledConquestEndTime: Optional[datetime]
    requiredVictoryTowns: Optional[int]
    shortRequiredVictoryTowns: Optional[int]

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
