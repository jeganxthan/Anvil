from pathlib import Path

from app.documents.loaders.base import BaseLoader


class LoaderRegistry:
    def __init__(self) -> None:
        self._loaders: list[BaseLoader] = []

    def register(self, loader: BaseLoader) -> None:
        self._loaders.append(loader)

    def resolve(self, source: str | Path) -> BaseLoader:
        for loader in self._loaders:
            if loader.supports(source):
                return loader

        raise ValueError(f"No loader found for '{source}'.")