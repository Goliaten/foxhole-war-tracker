from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/dynamic_data")


@router.get("/war_state/{shard_id}", response_model=None)
async def read_map_war_report(
    shard_id: int,
    war_number: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(status_code=501, detail="Endpoint not implemented.")


@router.get("/war_state/{shard_id}", response_model=None)
async def read_dynamic_map_data_from_to(
    shard_id: int,
    war_number: Optional[int] = None,
    datetime_from: Optional[int] = None,
    datetime_to: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(status_code=501, detail="Endpoint not implemented.")
