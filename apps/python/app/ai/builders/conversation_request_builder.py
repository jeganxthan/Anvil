from collections.abc import Sequence

from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.providers.schema.models import GenerateRequest



class ConversationRequestBuilder:

    def __init__(self, prompt_builder):
        self.prompt_builder = prompt_builder
    
    def build(self, conversation:Conversation, messages:Sequence[Message])->GenerateRequest:
        prompt=self.prompt_builder.build(conversation, messages)
        return GenerateRequest(
            provider=conversation.provider,
            model=conversation.model,
            messages=prompt)