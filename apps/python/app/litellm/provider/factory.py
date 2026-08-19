from app.litellm.provider.base import (
    BaseLLMProvider,
)
from app.litellm.provider.litellm_provider import (
    LiteLLMProvider,
)


class LLMFactory:

    def __init__(self):

        self._provider = LiteLLMProvider()

    def create(self) -> BaseLLMProvider:
        return self._provider