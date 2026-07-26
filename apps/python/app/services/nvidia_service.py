from sse_starlette.sse import EventSourceResponse
from app.core.client import CHAT_CONFIG
from app.core.utils import serialize_messages
from app.schemas.chat import ChatRequest, ChatResponse, Usage
from collections.abc import Sequence
from openai.types.chat import ChatCompletionMessageParam
from app.core.exceptions import internal_server_error
from openai import AsyncOpenAI
class NvidiaService:
    
    def __init__(self, client:AsyncOpenAI):
        self.client=client
        
    async def generate_stream(self, request: ChatRequest):
        messages = serialize_messages(request)    
        return EventSourceResponse(self.generate(messages))

    async def generate_chat(self, request: ChatRequest):
        messages = serialize_messages(request)
        try:
            response = await self.client.chat.completions.create(
                 messages=messages,
                 **CHAT_CONFIG
            )

            return ChatResponse(
                id=response.id,
                model=response.model,
                answer=response.choices[0].message.content or "",
                usage=Usage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens
                ) if response.usage else None
            )
        except Exception as e:
            internal_server_error(e)


    async def generate(self, messages:Sequence[ChatCompletionMessageParam]):

        stream = await self.client.chat.completions.create(
            messages=messages,
            stream=True,
            **CHAT_CONFIG
        )

        async for chunk in stream:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                yield {
                    "event": "message",
                    "data": delta
                }

        yield {
            "event": "end",
            "data": "[DONE]"
        }

