from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000

    database_url: str = Field(
        default="sqlite+aiosqlite:///anvil.db",
        validation_alias="DATABASE_URL",
    )

    # NVIDIA
    nvidia_api_url: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        validation_alias="NVIDIA_API_URL",
    )

    nvidia_api_key: str = Field(
        validation_alias="NVIDIA_API_KEY",
    )

    nvidia_model: str = Field(
        default="nvidia/llama-3.3-nemotron-super-49b-v1.5",
        validation_alias="NVIDIA_MODEL",
    )

    # Generation defaults
    temperature: float = Field(default=0.6, validation_alias="TEMPERATURE")

    max_tokens: int = Field(default=65536, validation_alias="MAX_TOKENS")

    top_p: float = Field(default=0.95, validation_alias="TOP_P")

    frequency_penalty: float = Field(
        default=0.0,
        validation_alias="FREQUENCY_PENALTY",
    )

    presence_penalty: float = Field(
        default=0.0,
        validation_alias="PRESENCE_PENALTY",
    )

    seed: int = Field(default=0, validation_alias="SEED")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()