from app.providers.schema.models import GenerateRequest, GenerateResponse, ProviderInfo
from collections.abc import AsyncIterator
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        pass

    @abstractmethod
    def get_provider_info(self) -> ProviderInfo:
        pass
    
    @abstractmethod
    async def generate_stream(self, request: GenerateRequest)-> AsyncIterator[str]:
        yield