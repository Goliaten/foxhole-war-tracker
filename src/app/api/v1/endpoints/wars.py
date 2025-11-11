from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.schemas import WarState
from src.app.schemas import Shard
from src.app.schemas import Hex
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter()


@router.get("/hex", response_model=List[Hex], tags=["hex"])
async def read_hexes(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all hexes.
    """
    hexes = await crud.get_hexes(db)
    return hexes


@router.get("/hex/{hex_id}", response_model=Hex, tags=["hex"])
async def read_hex(hex_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a hex by `id`.
    """
    hex = await crud.get_hex(db, id=hex_id)
    if hex is None:
        raise HTTPException(status_code=404, detail="Hex not found")
    return hex


@router.get("/shard", response_model=List[Shard], tags=["shard"])
async def read_shards(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all shards.
    """
    hexes = await crud.get_hexes(db)
    return hexes


@router.get("/shard/{shard_id}", response_model=Shard, tags=["shard"])
async def read_shard(shard_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a shard by `id`.
    """
    hex = await crud.get_hex(db, id=shard_id)
    if hex is None:
        raise HTTPException(status_code=404, detail="Shard not found")
    return hex


@router.get("/war_state/{shard_id}", response_model=WarState)
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


# @router.get("/", response_model=List[War])
# async def read_wars(
#     skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
# ):
#     """
#     Retrieve all wars, sorted by most recent.
#     """
#     wars = await crud.get_all_wars(db, skip=skip, limit=limit)
#     return wars


# @router.get("/{war_number}", response_model=War)
# async def read_war(war_number: int, db: AsyncSession = Depends(get_db)):
#     """
#     Retrieve a specific war by its number.
#     """
#     db_war = await crud.get_war_by_number(db, war_number=war_number)
#     if db_war is None:
#         raise HTTPException(status_code=404, detail="War not found")
#     return db_war
