from pydantic import BaseModel


class EmbeddingConfig(BaseModel):
    provider: str

    model: str

    api_key: str | None = None

    device: str = "cpu"