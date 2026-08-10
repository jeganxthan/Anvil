from langchain_core.output_parsers import PydanticOutputParser

from app.langchain.prompts.config.types import PromptType

from app.langchain.prompts.prompt_loader import PromptLoader
from app.langchain.prompts.prompt_build import PromptBuilder
from app.providers.base import BaseProvider
from app.schemas.summary import SummaryRequest, SummaryResponse


class SummaryService:

    def __init__(
        self,
        prompt_loader: PromptLoader,
        prompt_builder: PromptBuilder,
        provider: BaseProvider,
    ):
        self.prompt_loader = prompt_loader
        self.prompt_builder = prompt_builder
        self.provider = provider

    async def summarize(
        self,
        request: SummaryRequest,
    ) -> SummaryResponse:

        system_prompt = await self.prompt_loader.get_active(
            PromptType.SUMMARY
        )

        if system_prompt is None:
            raise ValueError(
                "No active summary prompt found."
            )

        parser = PydanticOutputParser(
            pydantic_object=SummaryResponse,
        )

        prompt = self.prompt_builder.build(
            system_prompt,
        )

        llm = self.provider.get_model(
            request.model
        )

        chain = (
            prompt
            | llm
            | parser
        )

        result = await chain.ainvoke(
            {
                "text": request.text,
                "format_instructions": parser.get_format_instructions(),
            }
        )

        return result