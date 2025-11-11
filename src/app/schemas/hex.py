from pydantic import BaseModel


class Hex(BaseModel):
    id: int
    REV: int
    name: str

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
