from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    #
    # Server
    #
    host: str = Field(
        default="127.0.0.1",
        validation_alias="HOST",
    )

    port: int = Field(
        default=8000,
        validation_alias="PORT",
    )


    #
    # Database
    #
    database_url: str = Field(
        default="sqlite+aiosqlite:///anvil.db",
        validation_alias="DATABASE_URL",
    )


    #
    # LiteLLM / Chat Model
    #
    llm_model: str = Field(
        default="gpt-4o-mini",
        validation_alias="LLM_MODEL",
    )

    llm_api_key: str | None = Field(
        default=None,
        validation_alias="LLM_API_KEY",
    )

    llm_base_url: str | None = Field(
        default=None,
        validation_alias="LLM_BASE_URL",
    )


    #
    # Chat Generation Defaults
    #
    temperature: float = Field(
        default=0.7,
        validation_alias="TEMPERATURE",
    )

    max_tokens: int = Field(
        default=4096,
        validation_alias="MAX_TOKENS",
    )

    top_p: float = Field(
        default=1.0,
        validation_alias="TOP_P",
    )


    #
    # Embeddings (for future RAG)
    #
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL",
    )

    embedding_device: str = Field(
        default="cpu",
        validation_alias="EMBEDDING_DEVICE",
    )


    #
    # Application
    #
    debug: bool = Field(
        default=False,
        validation_alias="DEBUG",
    )


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()