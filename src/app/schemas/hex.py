from pydantic import BaseModel
from typing import Optional


class Hex(BaseModel):
    id: int
    REV: Optional[int] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
