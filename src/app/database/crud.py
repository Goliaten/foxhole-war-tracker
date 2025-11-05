from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Type

from sqlalchemy import delete as sa_delete, insert as sa_insert
from sqlalchemy import select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession
# sqlalchemy.orm imports not needed here

from src.app.database.models import (
    REV,
    Hex,
    StructureTypes,
    Shard,
    WarState,
    MapWarReport,
    StaticMapData,
    StaticMapDataItem,
    DynamicMapData,
    DynamicMapDataItem,
)


# Generic helpers
async def _get_one(db: AsyncSession, model: Type[Any], **filters) -> Optional[Any]:
    stmt = select(model).filter_by(**filters)
    result = await db.execute(stmt)
    return result.scalars().first()


async def _get_many(
    db: AsyncSession, model: Type[Any], skip: int = 0, limit: int = 100, **filters
) -> List[Any]:
    stmt = select(model).filter_by(**filters).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def _delete(db: AsyncSession, model: Type[Any], **filters) -> int:
    stmt = sa_delete(model).filter_by(**filters)
    res = await db.execute(stmt)
    await db.commit()
    return res.rowcount if hasattr(res, "rowcount") else 0


async def _upsert(
    db: AsyncSession,
    model: Type[Any],
    key_fields: Iterable[str],
    data: Dict[str, Any],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> Any:
    """
    Upsert helper: find by key_fields; update if exists, insert otherwise.
    If strict_insert is True, raise if record exists.
    If strict_update is True, raise if no record exists to update.
    """
    # Prefer updating by primary key if present in data and not null/None.
    pk_filters = {k: data[k] for k in key_fields if k in data and data[k] is not None}

    if pk_filters:
        existing = await _get_one(db, model, **pk_filters)

        if existing and strict_insert:
            raise ValueError("Record exists but strict_insert=True")

        if not existing and strict_update:
            raise ValueError("Record does not exist but strict_update=True")

        if existing:
            # update by PK
            await db.execute(
                sa_update(model)
                .where(*[getattr(model, k) == pk_filters[k] for k in pk_filters])
                .values(**data)
            )
            await db.commit()
            return await _get_one(db, model, **pk_filters)

        # If PK present but no existing and strict_update is False, insert
        stmt = sa_insert(model).values(**data)
        await db.execute(stmt)
        await db.commit()
        return await _get_one(db, model, **pk_filters)

    # No PK present: perform insert (do not attempt to match by other keys)
    if strict_update:
        # caller expected an update by PK but none was provided
        raise ValueError("strict_update=True but no primary key provided in data")

    # Insert
    stmt = sa_insert(model).values(**data)
    await db.execute(stmt)
    await db.commit()
    # Try to return by any provided key_fields if possible, otherwise return None
    return await _get_one(db, model, **{k: data[k] for k in key_fields if k in data})


# Per-model CRUD wrappers


# REV
async def get_rev(db: AsyncSession, rev: int) -> Optional[REV]:
    return await _get_one(db, REV, REV=rev)


async def list_revs(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[REV]:
    return await _get_many(db, REV, skip=skip, limit=limit, **filters)


async def create_rev_and_get_id(db: AsyncSession) -> REV:
    rev = REV(tmstmp=datetime.now(timezone.utc))  # use utc time
    db.add(rev)
    await db.commit()
    await db.refresh(rev)  # populates rev.REV (autoincrement PK)
    return rev


async def upsert_rev(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["REV"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> REV:
    return await _upsert(
        db,
        REV,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_rev(db: AsyncSession, rev: int) -> int:
    return await _delete(db, REV, REV=rev)


# Hex
async def get_hex(db: AsyncSession, **filters) -> Optional[Hex]:
    return await _get_one(db, Hex, **filters)


async def list_hexes(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[Hex]:
    return await _get_many(db, Hex, skip=skip, limit=limit, **filters)


async def upsert_hex(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> Hex:
    return await _upsert(
        db,
        Hex,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_hex(db: AsyncSession, **filters) -> int:
    return await _delete(db, Hex, **filters)


# StructureTypes
async def get_structure_type(db: AsyncSession, **filters) -> Optional[StructureTypes]:
    return await _get_one(db, StructureTypes, **filters)


async def list_structure_types(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[StructureTypes]:
    return await _get_many(db, StructureTypes, skip=skip, limit=limit, **filters)


async def upsert_structure_type(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> StructureTypes:
    return await _upsert(
        db,
        StructureTypes,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_structure_type(db: AsyncSession, **filters) -> int:
    return await _delete(db, StructureTypes, **filters)


# Shard
async def get_shard(db: AsyncSession, **filters) -> Optional[Shard]:
    return await _get_one(db, Shard, **filters)


async def get_shard_by_url(db: AsyncSession, base_url: str) -> Optional[Shard]:
    return await _get_one(db, Shard, url=base_url)


async def list_shards(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[Shard]:
    return await _get_many(db, Shard, skip=skip, limit=limit, **filters)


async def upsert_shard(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> Shard:
    return await _upsert(
        db,
        Shard,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_shard(db: AsyncSession, **filters) -> int:
    return await _delete(db, Shard, **filters)


# WarState
async def get_warstate(db: AsyncSession, **filters) -> Optional[WarState]:
    return await _get_one(db, WarState, **filters)


async def list_warstates(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[WarState]:
    return await _get_many(db, WarState, skip=skip, limit=limit, **filters)


async def upsert_warstate(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> WarState:
    return await _upsert(
        db,
        WarState,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_warstate(db: AsyncSession, **filters) -> int:
    return await _delete(db, WarState, **filters)


# MapWarReport
async def get_map_war_report(db: AsyncSession, **filters) -> Optional[MapWarReport]:
    return await _get_one(db, MapWarReport, **filters)


async def list_map_war_reports(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[MapWarReport]:
    return await _get_many(db, MapWarReport, skip=skip, limit=limit, **filters)


async def upsert_map_war_report(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> MapWarReport:
    return await _upsert(
        db,
        MapWarReport,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_map_war_report(db: AsyncSession, **filters) -> int:
    return await _delete(db, MapWarReport, **filters)


# StaticMapData
async def get_static_map_data(db: AsyncSession, **filters) -> Optional[StaticMapData]:
    return await _get_one(db, StaticMapData, **filters)


async def list_static_map_data(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[StaticMapData]:
    return await _get_many(db, StaticMapData, skip=skip, limit=limit, **filters)


async def upsert_static_map_data(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> StaticMapData:
    return await _upsert(
        db,
        StaticMapData,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_static_map_data(db: AsyncSession, **filters) -> int:
    return await _delete(db, StaticMapData, **filters)


# StaticMapDataItem
async def get_static_map_data_item(
    db: AsyncSession, **filters
) -> Optional[StaticMapDataItem]:
    return await _get_one(db, StaticMapDataItem, **filters)


async def list_static_map_data_items(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[StaticMapDataItem]:
    return await _get_many(db, StaticMapDataItem, skip=skip, limit=limit, **filters)


async def upsert_static_map_data_item(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> StaticMapDataItem:
    return await _upsert(
        db,
        StaticMapDataItem,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_static_map_data_item(db: AsyncSession, **filters) -> int:
    return await _delete(db, StaticMapDataItem, **filters)


# DynamicMapData
async def get_dynamic_map_data(db: AsyncSession, **filters) -> Optional[DynamicMapData]:
    return await _get_one(db, DynamicMapData, **filters)


async def list_dynamic_map_data(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[DynamicMapData]:
    return await _get_many(db, DynamicMapData, skip=skip, limit=limit, **filters)


async def upsert_dynamic_map_data(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> DynamicMapData:
    return await _upsert(
        db,
        DynamicMapData,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_dynamic_map_data(db: AsyncSession, **filters) -> int:
    return await _delete(db, DynamicMapData, **filters)


# DynamicMapDataItem
async def get_dynamic_map_data_item(
    db: AsyncSession, **filters
) -> Optional[DynamicMapDataItem]:
    return await _get_one(db, DynamicMapDataItem, **filters)


async def list_dynamic_map_data_items(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[DynamicMapDataItem]:
    return await _get_many(db, DynamicMapDataItem, skip=skip, limit=limit, **filters)


async def upsert_dynamic_map_data_item(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields=["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> DynamicMapDataItem:
    return await _upsert(
        db,
        DynamicMapDataItem,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_dynamic_map_data_item(db: AsyncSession, **filters) -> int:
    return await _delete(db, DynamicMapDataItem, **filters)
