from typing import cast

from openai.types.chat import ChatCompletionMessageParam

from app.providers.schema.models import ChatMessage


def convert_messages(
    messages: list[ChatMessage],
) -> list[ChatCompletionMessageParam]:
    return [
        cast(
            ChatCompletionMessageParam,
            {
                "role": message.role.value,
                "content": message.content,
            },
        )
        for message in messages
    ]