from collections.abc import AsyncIterator
from app.core.enum import Provider
from app.providers.base import BaseProvider
from openai import AsyncOpenAI

from app.providers.schema.models import GenerateRequest, GenerateResponse, ProviderInfo
from app.providers.schema.models import Usage
from app.core.exceptions import InternalServerError
from app.providers.adapters.openai import convert_messages

class NvidiaProvider(BaseProvider):
    def __init__(self, client:AsyncOpenAI, settings):
        self.client = client
        self.settings = settings

    async def generate(self, request:GenerateRequest) -> GenerateResponse:
        try:
            response = await self.client.chat.completions.create(
                model=request.model or self.settings.nvidia_model,
                messages=convert_messages(request.messages),
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                frequency_penalty=request.frequency_penalty,
                presence_penalty=request.presence_penalty,
                seed=request.seed,
            )
            return GenerateResponse(
                id=response.id,
                provider=Provider.NVIDIA,
                model=response.model,
                content=response.choices[0].message.content or "",
                finish_reason=response.choices[0].finish_reason,
                usage=Usage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                )
                if response.usage
                else None,
            )
        except Exception as exc:
            raise InternalServerError(f"Failed to generate response: {exc}") from exc
    
    async def generate_stream(
        self,
        request: GenerateRequest,
    ) -> AsyncIterator[str]:

        try:
            stream = await self.client.chat.completions.create(
                model=request.model or self.settings.nvidia_model,
                messages=convert_messages(request.messages),
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                frequency_penalty=request.frequency_penalty,
                presence_penalty=request.presence_penalty,
                seed=request.seed,
                stream=True,
            )

            async for chunk in stream:

                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta.content

                if delta:
                    yield delta

        except Exception as exc:
            raise InternalServerError(
                "Failed to stream response."
            ) from exc

    async def get_provider_info(self) -> ProviderInfo:

        return ProviderInfo(
            provider=Provider.NVIDIA,
            model=self.settings.nvidia_model,
            context_window=131072,
            supports_streaming=True,
            supports_tools=True,
            supports_embeddings=False,
            supports_vision=False,
            supports_audio=False,
        )