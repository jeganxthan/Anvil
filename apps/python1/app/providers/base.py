from abc import ABC, abstractmethod
from typing import Any

from app.core.enum import Provider


class BaseProvider(ABC):

    @property
    @abstractmethod
    def provider(self) -> Provider:
        pass


    @abstractmethod
    def get_model(
        self,
        model: str | None = None,
    ) -> Any:
        pass