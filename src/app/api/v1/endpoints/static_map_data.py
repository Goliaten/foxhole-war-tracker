from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/static_data")


@router.get("/{shard_id}", response_model=None)
async def read_static_map_data(
    shard_id: int, war_number: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    raise HTTPException(status_code=501, detail="Endpoint not implemented.")


@router.get("/{shard_id}", response_model=None)
async def read_static_map_data_from_to(
    shard_id: int,
    war_number: Optional[int] = None,
    timestamp_from: Optional[int] = None,
    timestamp_to: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(status_code=501, detail="Endpoint not implemented.")
