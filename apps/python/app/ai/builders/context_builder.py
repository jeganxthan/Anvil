from app.ai.context.models import PromptContext
from app.core.enum import MessageRole
from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.providers.schema.models import ChatMessage


class ContextBuilder:

    def build(
        self,
        conversation: Conversation,
        messages: list[Message],
    ) -> PromptContext:

        prompt_messages: list[ChatMessage] = []

        if conversation.system_prompt:
            prompt_messages.append(
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content=conversation.system_prompt,
                )
            )

        prompt_messages.extend(
            ChatMessage(
                role=message.role,
                content=message.content,
            )
            for message in messages
        )

        return PromptContext(
            messages=prompt_messages,
        )