from app.db.models.llm_model import LLMModel
from app.litellm.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
)
from app.litellm.provider.factory import LLMFactory
from app.services.llm_model_service import LLMModelService



class LLMService:

    def __init__(
        self,
        factory: LLMFactory,
        model_service: LLMModelService,
    ):
        self.provider = factory.create()
        self.model_service = model_service

    async def _build_request(
        self,
        request: ChatRequest,
        model: LLMModel,
    ) -> ChatRequest:

        return ChatRequest(
            model=model.model,
            api_base=model.api_base,
            api_key=model.api_key,
            messages=request.messages,
            temperature=model.temperature,
            max_tokens=model.max_tokens,
            top_p=model.top_p,
            frequency_penalty=model.frequency_penalty,
            presence_penalty=model.presence_penalty,
            seed=request.seed,
        )

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        model = await self.model_service.get_active()

        if model is None:
            raise ValueError(
                "No active LLM model configured",
            )

        resolved_request = await self._build_request(
            request,
            model,
        )

        return await self.provider.chat(
            resolved_request,
        )

    async def stream(
        self,
        request: ChatRequest,
    ):
        model = await self.model_service.get_active()

        if model is None:
            raise ValueError(
                "No active LLM model configured",
            )

        resolved_request = await self._build_request(
            request,
            model,
        )

        async for chunk in self.provider.stream(
            resolved_request,
        ):
            yield chunk