from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from app.core.utils import serialize_messages
from app.schemas.chat import ChatRequest, ChatResponse, Usage
from app.core.exceptions import InternalServerError

class NvidiaService:
    def __init__(self, client: AsyncOpenAI, chat_config: dict):
        self.client = client
        self.chat_config = chat_config

    async def generate_chat(self, request: ChatRequest) -> ChatResponse:
        messages = serialize_messages(request)
        try:
            response = await self.client.chat.completions.create(
                messages=messages, **self.chat_config
            )

            return ChatResponse(
                id=response.id,
                model=response.model,
                answer=response.choices[0].message.content or "",
                usage=Usage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                )
                if response.usage
                else None,
            )
        except Exception as e:
            raise InternalServerError(
                "Failed to generate chat response"
            ) from e

    async def generate_stream(self, request: ChatRequest) -> AsyncGenerator[dict, None]:
        messages = serialize_messages(request)
        stream = await self.client.chat.completions.create(
            messages=messages, stream=True, **self.chat_config
        )

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                yield {"event": "message", "data": delta}

        yield {"event": "end", "data": "[DONE]"}
