from datetime import datetime
from pydantic import BaseModel


class REV(BaseModel):
    REV: int
    tmstmp: datetime

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
