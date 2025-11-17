from pydantic import BaseModel


class StaticMapData(BaseModel):
    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
