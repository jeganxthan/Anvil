from typing import cast

from openai.types.chat import ChatCompletionMessageParam

from app.schemas.chat import ChatRequest


def serialize_messages(
    request: ChatRequest,
) -> list[ChatCompletionMessageParam]:
    return cast(
        list[ChatCompletionMessageParam],
        [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.messages
        ],
    )
