from app.db.database import get_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker
)
engine = get_engine()
Session = async_sessionmaker(
    engine,
    class_=AsyncSession
    )