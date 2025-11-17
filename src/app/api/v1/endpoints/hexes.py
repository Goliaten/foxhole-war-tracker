from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.app.schemas import Hex
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/hex")


# ---- hex ----
@router.get("/", response_model=List[Hex], tags=["hex"])
async def read_hexes(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all hexes.
    """
    hexes = await crud.list_hexes(db, skip=skip, limit=limit)
    return hexes


@router.get("/{hex_id}", response_model=Hex, tags=["hex"])
async def read_hex(hex_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a hex by `id`.
    """
    hex = await crud.get_hex(db, id=hex_id)
    if hex is None:
        raise HTTPException(status_code=404, detail="Hex not found")
    return hex
