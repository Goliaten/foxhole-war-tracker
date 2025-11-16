from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.app.schemas import WarState
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/war_state")


# ---- war_state ----
@router.get("/{shard_id}", response_model=WarState)
async def read_war_state(
    shard_id: int, war_number: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    """
    Get state of war for given shard.
    If no `war_number` is given, the currently active war is returned.
    If `war_number` is given, then the last state of given war is given, as long as that war_number is in database.
    """
    filters = {}
    if war_number:
        filters["warNumber"] = war_number

    warstate = await crud.get_warstate_latest(db, shard_id=shard_id, **filters)
    if warstate is None:
        raise HTTPException(status_code=404, detail="Warstate not found.")
    return warstate


@router.get("/{shard_id}", response_model=WarState)
async def read_war_state_from_to(
    shard_id: int,
    war_number: Optional[int] = None,
    timestamp_from: Optional[int] = None,
    timestamp_to: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(status_code=501, detail="Endpoint not implemented.")
