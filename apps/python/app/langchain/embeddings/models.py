from pydantic import BaseModel, Field


class EmbeddingConfig(BaseModel):
    model: str = "BAAI/bge-small-en-v1.5"

    device: str = "cpu"

    normalize: bool = True

    batch_size: int = 32

    model_kwargs: dict[str, object] = Field(
        default_factory=dict,
    )

    encode_kwargs: dict[str, object] = Field(
        default_factory=dict,
    )