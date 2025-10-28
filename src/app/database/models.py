from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app.database.session import Base


class War(Base):
    __tablename__ = "wars"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    war_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    start_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    winner: Mapped[str] = mapped_column(String(50), nullable=True)
    shard: Mapped[str] = mapped_column(String(255), nullable=True)

    regions_history = relationship("WarRegionsHistory", back_populates="war")
    structure_history = relationship("StructureHistory", back_populates="war")
    hex_statistics = relationship("HexStatisticHistory", back_populates="war")


class Hex(Base):
    __tablename__ = "hex"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)

    regions = relationship("Region", back_populates="hex")
    hex_statistics = relationship("HexStatisticHistory", back_populates="hex")


class Region(Base):
    __tablename__ = "regions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    map_name: Mapped[str] = mapped_column(String(100), nullable=True)
    region_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    hex_id: Mapped[int] = mapped_column(Integer, ForeignKey("hex.id"), nullable=True)

    hex = relationship("Hex", back_populates="regions")
    war_history = relationship("WarRegionsHistory", back_populates="region")
    structure_history = relationship("StructureHistory", back_populates="region")


class WarRegionsHistory(Base):
    __tablename__ = "war_regions_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    war_id: Mapped[int] = mapped_column(Integer, ForeignKey("wars.id"), nullable=True)
    region_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("regions.id"), nullable=True
    )
    owner: Mapped[str] = mapped_column(String(50), nullable=True)
    is_victory_town: Mapped[bool] = mapped_column(Boolean, nullable=True)

    war = relationship("War", back_populates="regions_history")
    region = relationship("Region", back_populates="war_history")


class StructureHistory(Base):
    __tablename__ = "structure_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    region_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("regions.id"), nullable=True
    )
    war_id: Mapped[int] = mapped_column(Integer, ForeignKey("wars.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    coordinates: Mapped[str] = mapped_column(String(255), nullable=True)
    controlling_faction: Mapped[str] = mapped_column(String(50), nullable=True)
    is_victory_town: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_scorched: Mapped[bool] = mapped_column(Boolean, nullable=True)

    region = relationship("Region", back_populates="structure_history")
    war = relationship("War", back_populates="structure_history")
    structure_types = relationship("StructureType", back_populates="town")


class StructureType(Base):
    __tablename__ = "structure_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    town_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("structure_history.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    town = relationship("StructureHistory", back_populates="structure_types")


class HexStatisticHistory(Base):
    __tablename__ = "hex_statistic_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    colonial_casualties: Mapped[int] = mapped_column(Integer, nullable=True)
    warden_casualties: Mapped[int] = mapped_column(Integer, nullable=True)
    total_enlistments: Mapped[int] = mapped_column(Integer, nullable=True)
    hex_id: Mapped[int] = mapped_column(Integer, ForeignKey("hex.id"), nullable=True)
    war_id: Mapped[int] = mapped_column(Integer, ForeignKey("wars.id"), nullable=True)

    hex = relationship("Hex", back_populates="hex_statistics")
    war = relationship("War", back_populates="hex_statistics")
