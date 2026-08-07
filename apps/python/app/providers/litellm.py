from langchain_litellm import ChatLiteLLM

from app.core.settings import Settings
from app.core.enum import Provider
from app.providers.base import BaseProvider


class LiteLLMProvider(BaseProvider):

    def __init__(
        self,
        settings: Settings,
    ):
        self.settings = settings


    @property
    def provider(self) -> Provider:
        return Provider.LITELLM


    def get_model(
        self,
        model: str | None = None,
    ):

        kwargs = {
            "model": model or self.settings.llm_model,
            "api_key": self.settings.llm_api_key,
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
            "top_p": self.settings.top_p,
        }


        if self.settings.llm_base_url:
            kwargs["api_base"] = self.settings.llm_base_url


        return ChatLiteLLM(
            **kwargs
        )