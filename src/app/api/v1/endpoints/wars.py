from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.app.database import crud
from src.app.database.session import get_db
from src.app.schemas.war import War

router = APIRouter()


@router.get("/", response_model=List[War])
async def read_wars(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all wars, sorted by most recent.
    """
    wars = await crud.get_all_wars(db, skip=skip, limit=limit)
    return wars


@router.get("/{war_number}", response_model=War)
async def read_war(war_number: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific war by its number.
    """
    db_war = await crud.get_war_by_number(db, war_number=war_number)
    if db_war is None:
        raise HTTPException(status_code=404, detail="War not found")
    return db_war
