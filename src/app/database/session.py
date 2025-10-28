from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from fastapi import Depends
from typing import AsyncGenerator

from src.app.core.config import settings

# Create the async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Create a sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for our SQLAlchemy models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get a DB session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
