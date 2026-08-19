from pydantic import BaseModel, ConfigDict, Field, SecretStr


class LLMModelBase(BaseModel):
    model: str

    api_base: str | None = None

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
    )

    top_p: float = Field(
        default=0.7,
        gt=0.0,
        le=1.0,
    )

    frequency_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
    )

    presence_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=1024,
        gt=0,
    )

    stream: bool = False


class LLMModelCreate(LLMModelBase):
    api_key: SecretStr | None = None
    is_active: bool = False


class LLMModelUpdate(BaseModel):
    model: str | None = None
    api_base: str | None = None

    api_key: SecretStr | None = None

    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
    )

    top_p: float | None = Field(
        default=None,
        gt=0.0,
        le=1.0,
    )

    frequency_penalty: float | None = Field(
        default=None,
        ge=-2.0,
        le=2.0,
    )

    presence_penalty: float | None = Field(
        default=None,
        ge=-2.0,
        le=2.0,
    )

    max_tokens: int | None = Field(
        default=None,
        gt=0,
    )

    stream: bool | None = None
    is_active: bool | None = None


class LLMModelResponse(LLMModelBase):
    id: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )