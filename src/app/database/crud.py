from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.database.models import War
from src.app.schemas.war import WarBase
from datetime import datetime


async def get_war_by_number(db: AsyncSession, war_number: int) -> War | None:
    """
    Fetches a single war by its war number.
    """
    result = await db.execute(select(War).where(War.war_number == war_number))
    return result.scalars().first()


async def get_all_wars(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[War]:
    """
    Fetches all wars with pagination.
    """
    result = await db.execute(
        select(War).order_by(War.war_number.desc()).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def create_or_update_war(db: AsyncSession, war_data: dict) -> War:
    """
    Updates a war if it exists by war_number, or creates it if it doesn't.
    This is an "upsert" operation.
    """
    # Convert timestamps from ms to datetime objects
    start_time = (
        datetime.fromtimestamp(war_data["conquestStartTime"] / 1000.0)
        if war_data.get("conquestStartTime")
        else None
    )
    end_time = (
        datetime.fromtimestamp(war_data["conquestEndTime"] / 1000.0)
        if war_data.get("conquestEndTime")
        else None
    )

    # Find existing war
    db_war = await get_war_by_number(db, war_number=war_data["warNumber"])

    if db_war:
        # Update existing war
        db_war.winner = war_data.get("winner")
        db_war.end_time = end_time
        # In case the start time was missing before
        if not db_war.start_time:
            db_war.start_time = start_time
    else:
        # Create new war
        db_war = War(
            war_number=war_data["warNumber"],
            start_time=start_time,
            end_time=end_time,
            winner=war_data.get("winner"),
            shard="live",  # The API doesn't seem to provide this, so we hardcode
        )
        db.add(db_war)

    await db.commit()
    await db.refresh(db_war)
    return db_war
