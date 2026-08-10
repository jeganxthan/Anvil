from pydantic import BaseModel, ConfigDict, SecretStr


class EmbeddingModelBase(BaseModel):
    provider: str
    model: str
    dimension: int
    device: str = "cpu"
    normalize: bool = True
    batch_size: int = 32


class EmbeddingModelCreate(EmbeddingModelBase):
    api_key: SecretStr | None = None
    is_active: bool = False


class EmbeddingModelUpdate(BaseModel):
    provider: str | None = None
    model: str | None = None
    dimension: int | None = None
    api_key: SecretStr | None = None
    device: str | None = None
    normalize: bool | None = None
    batch_size: int | None = None
    is_active: bool | None = None


class EmbeddingModelResponse(EmbeddingModelBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
