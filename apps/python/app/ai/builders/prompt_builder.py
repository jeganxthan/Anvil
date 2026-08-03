from app.providers.schema.models import ChatMessage
from app.ai.context.models import PromptContext

class PromptBuilder:

    def build(
        self,
        context: PromptContext,
    ) -> list[ChatMessage]:

        return context.messages