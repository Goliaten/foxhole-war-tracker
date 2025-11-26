from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.app.schemas import REV
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/rev")


# ---- hex ----
@router.get("/{rev_id}", response_model=REV, tags=["rev"])
async def read_rev_by_id(rev_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve rev by id.
    """
    rev = await crud.get_rev(db, rev=rev_id)
    if rev is None:
        raise HTTPException(status_code=404, detail="Rev not found")
    return rev


@router.get("/timestamp/{timestamp}", response_model=REV, tags=["rev"])
async def read_hex_by_date(timestamp: datetime, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a rev by datetime.
    It returns closest rev lower than given/equal datetime.
    """
    rev = await crud.get_rev_by_timestamp(db, timestamp=timestamp)
    if rev is None:
        raise HTTPException(status_code=404, detail="Rev not found")
    return rev
