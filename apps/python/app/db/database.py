from sqlalchemy.ext.asyncio import( create_async_engine,async_sessionmaker, AsyncSession
)
from app.core.client import settings

engine = create_async_engine(settings.database_url, connect_args={"autocommit": False})

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()