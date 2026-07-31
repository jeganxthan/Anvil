from sqlalchemy.ext.asyncio import create_async_engine

def get_engine():
    engine = create_async_engine(
    "sqlite+aiosqlite:///anvil.db", connect_args={"autocommit": False}
    )
    return engine