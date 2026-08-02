from app.core.enum import Provider
from app.providers.base import BaseProvider


class ProviderRegistry:
    def __init__(self):
        self._providers: dict[Provider, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        info = provider.get_provider_info()
        self._providers[info.provider] = provider

    def get(self, provider: Provider) -> BaseProvider:
        return self._providers[provider]