from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from app.langchain.prompts.config.types import PromptType

class SystemPromptBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
    )

    template: str = Field(
        min_length=1,
        max_length=100_000,
    )

    type: PromptType
    is_active: bool = True


class SystemPromptCreate(SystemPromptBase):
    pass

class SystemPromptResponse(SystemPromptBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )