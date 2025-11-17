from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.app.schemas import Shard
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/shard")


@router.get("/", response_model=List[Shard], tags=["shard"])
async def read_shards(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all shards.
    """
    hexes = await crud.list_shards(db, skip=skip, limit=limit)
    return hexes


@router.get("/{shard_id}", response_model=Shard, tags=["shard"])
async def read_shard(shard_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a shard by `id`.
    """
    hex = await crud.get_shard(db, id=shard_id)
    if hex is None:
        raise HTTPException(status_code=404, detail="Shard not found")
    return hex
