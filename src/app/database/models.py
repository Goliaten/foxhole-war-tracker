from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app.database.session import Base


# Models derived from bb.sql


class REV(Base):
    __tablename__ = "REV"
    REV: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmstmp: Mapped[DateTime] = mapped_column(DateTime)


class Hex(Base):
    __tablename__ = "hex"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    name: Mapped[str] = mapped_column(String(150))

    rev = relationship("REV")


class StructureTypes(Base):
    __tablename__ = "StructureTypes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    name: Mapped[str] = mapped_column(String(50))

    rev = relationship("REV")


class Shard(Base):
    __tablename__ = "shard"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    url: Mapped[str] = mapped_column(String(200))
    name: Mapped[str] = mapped_column(String(20), nullable=True)

    rev = relationship("REV")


class WarState(Base):
    __tablename__ = "WarState"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    shard_id: Mapped[int] = mapped_column(Integer, ForeignKey("shard.id"))
    warId: Mapped[str] = mapped_column(String(40), nullable=True)
    warNumber: Mapped[int] = mapped_column(Integer)
    winner: Mapped[str] = mapped_column(String(20), nullable=True)
    conquestStartTime: Mapped[DateTime] = mapped_column(DateTime)
    conquestEndTime: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    resistanceStartTime: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    scheduledConquestEndTime: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    requiredVictoryTowns: Mapped[int] = mapped_column(Integer, nullable=True)
    shortRequiredVictoryTowns: Mapped[int] = mapped_column(Integer, nullable=True)

    rev = relationship("REV")
    shard = relationship("Shard")


class MapWarReport(Base):
    __tablename__ = "MapWarReport"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    hex_id: Mapped[int] = mapped_column(Integer, ForeignKey("hex.id"))
    shard_id: Mapped[int] = mapped_column(Integer, ForeignKey("shard.id"))
    totalEnlistments: Mapped[int] = mapped_column(Integer, nullable=True)
    colonialCasualties: Mapped[int] = mapped_column(Integer, nullable=True)
    wardenCasualties: Mapped[int] = mapped_column(Integer, nullable=True)
    dayOfWar: Mapped[int] = mapped_column(Integer, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=True)

    rev = relationship("REV")
    hex = relationship("Hex")
    shard = relationship("Shard")


class StaticMapData(Base):
    __tablename__ = "StaticMapData"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    hex_id: Mapped[int] = mapped_column(Integer, ForeignKey("hex.id"))
    shard_id: Mapped[int] = mapped_column(Integer, ForeignKey("shard.id"))
    regionId: Mapped[int] = mapped_column(Integer, nullable=True)
    scorchedVictoryTowns: Mapped[int] = mapped_column(Integer, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=True)

    rev = relationship("REV")
    hex = relationship("Hex")
    shard = relationship("Shard")
    items = relationship(
        "StaticMapDataItem", back_populates="static_map", cascade="all, delete-orphan"
    )


class StaticMapDataItem(Base):
    __tablename__ = "StaticMapDataItem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    StaticMapData_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("StaticMapData.id")
    )
    text: Mapped[str] = mapped_column(String(150), nullable=True)
    x: Mapped[float] = mapped_column(Float, nullable=True)
    y: Mapped[float] = mapped_column(Float, nullable=True)
    mapMarkerType: Mapped[str] = mapped_column(String(6), nullable=True)

    rev = relationship("REV")
    static_map = relationship("StaticMapData", back_populates="items")


class DynamicMapData(Base):
    __tablename__ = "DynamicMapData"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    hex_id: Mapped[int] = mapped_column(Integer, ForeignKey("hex.id"))
    shard_id: Mapped[int] = mapped_column(Integer, ForeignKey("shard.id"))
    regionId: Mapped[int] = mapped_column(Integer, nullable=True)
    scorchedVictoryTowns: Mapped[int] = mapped_column(Integer, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=True)

    rev = relationship("REV")
    hex = relationship("Hex")
    shard = relationship("Shard")
    items = relationship(
        "DynamicMapDataItem", back_populates="dynamic_map", cascade="all, delete-orphan"
    )


class DynamicMapDataItem(Base):
    __tablename__ = "DynamicMapDataItem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    DynamicMapData_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("DynamicMapData.id")
    )
    teamId: Mapped[str] = mapped_column(String(20), nullable=True)
    iconType: Mapped[int] = mapped_column(
        Integer, ForeignKey("StructureTypes.id"), nullable=True
    )
    x: Mapped[float] = mapped_column(Float, nullable=True)
    y: Mapped[float] = mapped_column(Float, nullable=True)
    flags: Mapped[int] = mapped_column(Integer, nullable=True)
    viewDirection: Mapped[int] = mapped_column(Integer, nullable=True)

    rev = relationship("REV")
    dynamic_map = relationship("DynamicMapData", back_populates="items")
