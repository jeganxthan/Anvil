from abc import ABC, abstractmethod
from app.litellm.models import ChatRequest, ChatResponse


class BaseLLMProvider(ABC):

    @abstractmethod
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        ...

    @abstractmethod
    async def stream(
        self,
        request: ChatRequest,
    ):
        ...