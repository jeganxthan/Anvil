from datetime import datetime

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.langchain.prompts.config.types import PromptType
from app.langchain.prompts.prompt_loader import PromptLoader
from app.langchain.prompts.prompt_build import PromptBuilder

from app.providers.base import BaseProvider
from app.langchain.parsers.factory import OutputParserFactory


class ChatService:


    def __init__(
        self,
        prompt_loader: PromptLoader,
        prompt_builder: PromptBuilder,
        provider: BaseProvider,
    ):
        self.prompt_loader = prompt_loader
        self.prompt_builder = prompt_builder
        self.provider = provider


    async def chat(
        self,
        data: ChatRequest,
    ) -> ChatResponse:


        # 1. Load active system prompt

        system_prompt = await self.prompt_loader.get_active(
            PromptType.SYSTEM
        )


        if system_prompt is None:
            raise ValueError(
                "No active system prompt found"
            )


        # 2. Get LangChain chat model

        llm = self.provider.get_model(
            data.model
        )


        # 3. Select output parser

        parser = OutputParserFactory.create(
            "string"
        )


        # 4. Build prompt

        prompt = self.prompt_builder.build(
            system_prompt,
        )


        # 5. Create LangChain chain

        chain = (
            prompt
            | llm
            | parser
        )


        # 6. Invoke chain

        content = await chain.ainvoke(
        {
            "question": data.message,
            "format_instructions":
                parser.get_format_instructions(),
        }
    )


        # 7. Return API response

        return ChatResponse(
            id="chat-response",
            provider=self.provider.provider,
            model=data.model or "",
            content=content,
            finish_reason=None,
            created_at=datetime.utcnow(),
        )