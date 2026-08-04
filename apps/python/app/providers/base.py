from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.providers.schema.models import GenerateRequest, GenerateResponse, ProviderInfo

class BaseProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        """
        Generate a complete response.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_stream(
        self,
        request: GenerateRequest,
    ) -> AsyncIterator[str]:
        """
        Stream the generated response chunk by chunk.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def info(self) -> ProviderInfo:
        """
        Static metadata describing this provider.
        """
        raise NotImplementedError