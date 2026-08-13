from abc import ABC, abstractmethod
from app.ai.context.model import ContextDocument



class ContextOrdering(ABC):

    @abstractmethod
    def order(
        self,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:
        ...


class PreserveOrder(ContextOrdering):

    def order(
        self,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:
        return documents