from pydantic import BaseModel


class DynamicMapData(BaseModel):
    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
