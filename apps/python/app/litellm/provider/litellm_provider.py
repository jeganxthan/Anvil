import litellm

from app.litellm.models import (
    ChatRequest,
    ChatResponse,
)
from app.litellm.provider.base import (
    BaseLLMProvider,
)


litellm.drop_params = True


class LiteLLMProvider(BaseLLMProvider):

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.messages
        ]

        kwargs = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "frequency_penalty": request.frequency_penalty,
            "presence_penalty": request.presence_penalty,
        }

        if request.api_base is not None:
            kwargs["api_base"] = request.api_base

        if request.api_key is not None:
            kwargs["api_key"] = request.api_key

        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens

        if request.seed is not None:
            kwargs["seed"] = request.seed

        response = await litellm.acompletion(
            **kwargs,
        )

        choice = response.choices[0]

        usage = None

        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        return ChatResponse(
            content=choice.message.content or "",
            model=response.model,
            usage=usage,
        )

    async def stream(
        self,
        request: ChatRequest,
    ):

        messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.messages
        ]

        kwargs = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "frequency_penalty": request.frequency_penalty,
            "presence_penalty": request.presence_penalty,
            "stream": True,
        }

        if request.api_base is not None:
            kwargs["api_base"] = request.api_base

        if request.api_key is not None:
            kwargs["api_key"] = request.api_key

        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens

        if request.seed is not None:
            kwargs["seed"] = request.seed

        response = await litellm.acompletion(
            **kwargs,
        )

        async for chunk in response:

            if not chunk.choices:
                continue

            content = getattr(
                chunk.choices[0].delta,
                "content",
                None,
            )

            if content:
                yield content