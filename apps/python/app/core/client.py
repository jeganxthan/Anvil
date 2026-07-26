from openai import AsyncOpenAI
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000

    nvidia_api_url: str = "https://integrate.api.nvidia.com/v1"

    nvidia_api_key: str = Field(
        validation_alias="NVIDIA_API_KEY"
    )

    model_name: str = "nvidia/llama-3.3-nemotron-super-49b-v1.5"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


CHAT_CONFIG = {
    "model": settings.model_name,
    "max_tokens": 65536,
    "temperature": 0.6,
    "top_p": 0.95,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "seed": 0,
}