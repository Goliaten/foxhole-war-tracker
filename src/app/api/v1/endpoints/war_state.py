from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.core.config import settings
from src.app.schemas import WarState
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/war_state")


@router.get("/range/{shard_id}", response_model=List[WarState], tags=["war_state"])
@router.get(
    "/range/{shard_id}/{war_number}", response_model=List[WarState], tags=["war_state"]
)
async def read_war_state_from_to(
    shard_id: int,
    datetime_from: datetime,
    datetime_to: datetime,
    war_number: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    filters = {"shard_id": shard_id}
    if war_number:
        filters["warNumber"] = war_number

    if datetime_from >= datetime_to:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime range. `from` should be smaller than `to`.",
        )

    warstates = await crud.list_warstates_REV(
        db,
        datetime_from=datetime_from,
        datetime_to=datetime_to,
        skip=skip,
        limit=limit,
        **filters,
    )
    if not warstates:
        raise HTTPException(status_code=404, detail="Warstates not found.")
    return warstates


@router.get("/{shard_id}", response_model=WarState, tags=["war_state"])
@router.get("/{shard_id}/{war_number}", response_model=WarState, tags=["war_state"])
async def read_war_state(
    shard_id: int, war_number: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    """
    Get state of war for given shard.
    If no `war_number` is given, the currently active war is returned.
    If `war_number` is given, then the last state of given war is given, as long as that war_number is in database.
    """
    filters = {"shard_id": shard_id}
    if war_number:
        filters["warNumber"] = war_number

    warstate = await crud.get_warstate_latest(db, **filters)
    if warstate is None:
        raise HTTPException(status_code=404, detail="Warstate not found.")
    return warstate
