from pydantic import BaseModel


class MapWarReport(BaseModel):
    id: int
    REV: int
    hex_id: int
    shard_id: int
    totalEnlistments: int
    colonialCasualties: int
    wardenCasualties: int
    dayOfWar: int
    version: int

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
