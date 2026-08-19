from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    
    # DATABASE
    database_url: str = Field(
        default="sqlite+aiosqlite:///anvil.db",
        validation_alias="DATABASE_URL",
    )
    
    sqlite_vec_path: str = Field(
        default="anvil.db",
        validation_alias="SQLITE_PATH",
    )
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }
    
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()