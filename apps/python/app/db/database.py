from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "sqlite+aiosqlite:///myfile.db", connect_args={"autocommit": False}
)