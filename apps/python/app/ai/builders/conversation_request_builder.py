from collections.abc import Sequence

from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.providers.schema.models import ChatMessage, GenerateRequest



class ConversationRequestBuilder:

    def build(
        self,
        conversation: Conversation,
        messages: Sequence[Message],
    ) -> GenerateRequest:

        return GenerateRequest(
            provider=conversation.provider,
            model=conversation.model,
            messages=[
                ChatMessage(
                    role=message.role,
                    content=message.content,
                )
                for message in messages
            ],
        )