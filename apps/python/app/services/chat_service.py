from datetime import datetime

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.langchainDummy.prompts.config.types import PromptType


class ChatService:

    def __init__(
        self,
        prompt_loader,
        prompt_builder,
        provider,
    ):
        self.prompt_loader = prompt_loader
        self.prompt_builder = prompt_builder
        self.provider = provider


    async def chat(
        self,
        data: ChatRequest,
    ) -> ChatResponse:


        # 1. Get active prompt from database

        system_prompt = await self.prompt_loader.get_active(
            PromptType.SYSTEM
        )


        if system_prompt is None:
            raise ValueError(
                "No active system prompt found"
            )


        # 2. Build ChatPromptTemplate

        prompt = self.prompt_builder.build(
            system_prompt
        )


        # 3. Convert template into messages

        messages = prompt.format_messages(
            question=data.message
        )


        # 4. Get LangChain chat model

        llm = self.provider.get_model(
            data.model
        )


        # 5. Invoke model

        response = await llm.ainvoke(
            messages
        )


        # response is AIMessage

        return ChatResponse(
            id="chat-response",
            provider=self.provider.provider,
            model=data.model or "",
            content=response.content,
            finish_reason=None,
            created_at=datetime.utcnow(),
        )