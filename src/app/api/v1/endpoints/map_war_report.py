from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.schemas import MapWarReport
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/map_report")


@router.get(
    "/range/{shard_id}",
    response_model=List[MapWarReport],
    tags=["map_war_report"],
)
@router.get(
    "/range/{shard_id}/{hex_id}",
    response_model=List[MapWarReport],
    tags=["map_war_report"],
)
async def read_map_war_report_from_to(
    shard_id: int,
    datetime_from: datetime,
    datetime_to: datetime,
    hex_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    filters = {"shard_id": shard_id}
    if hex_id:
        filters["hex_id"] = hex_id

    if datetime_from >= datetime_to:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime range. `from` should be smaller than `to`.",
        )

    mapwarreports = await crud.list_map_war_reports_REV(
        db,
        datetime_from=datetime_from,
        datetime_to=datetime_to,
        skip=skip,
        limit=limit,
        **filters,
    )
    if not mapwarreports:
        raise HTTPException(status_code=404, detail="Map war reports not found.")
    return mapwarreports


@router.get(
    "/{shard_id}/{hex_id}",
    response_model=MapWarReport,
    tags=["map_war_report"],
)
async def read_map_war_report(
    shard_id: int, hex_id: int, db: AsyncSession = Depends(get_db)
):
    """ """
    filters = {"shard_id": shard_id, "hex_id": hex_id}

    warstate = await crud.get_map_war_report_latest(db, **filters)
    if warstate is None:
        raise HTTPException(status_code=404, detail="Warstate not found.")
    return warstate


@router.get(
    "/{shard_id}",
    response_model=List[MapWarReport],
    tags=["map_war_report"],
)
async def read_map_war_report_all_hexes(
    shard_id: int, db: AsyncSession = Depends(get_db)
):
    """ """
    filters = {"shard_id": shard_id}

    warstate = await crud.list_map_war_report_latest(db, **filters)
    if warstate is None:
        raise HTTPException(status_code=404, detail="Warstate not found.")
    return warstate
