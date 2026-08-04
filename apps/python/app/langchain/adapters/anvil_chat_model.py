from collections.abc import Mapping
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app.core.enum import Provider
from app.providers.registry import ProviderRegistry
from app.providers.schema.models import GenerateRequest
from app.langchain.adapters.messages import MessageAdapter


class AnvilChatModel(BaseChatModel):
    def __init__(
        self,
        provider_registry: ProviderRegistry,
        provider: Provider,
        model: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        self.provider_registry = provider_registry
        self.provider = provider
        self.model = model
    
    @property
    def _llm_type(self)->str:
        return "anvil"
    
    async def _generate(self, messages:list[BaseMessage]):
        chat_messages=MessageAdapter.to_chat_messages(messages)
        request = GenerateRequest(
            model=self.provider,
            model=self.model,
            mess
        )