from typing import Literal
from app.ai.context.model import ContextDocument



class ContextFilter:

    def __init__(
        self,
        threshold: float | None = None,
        mode: Literal["higher", "lower"] = "higher",
    ):
        self.threshold = threshold
        self.mode = mode

    def filter(
        self,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:

        if self.threshold is None:
            return documents

        filtered: list[ContextDocument] = []

        for document in documents:
            if document.score is None:
                continue

            if self.mode == "higher":
                if document.score >= self.threshold:
                    filtered.append(document)

            else:
                if document.score <= self.threshold:
                    filtered.append(document)

        return filtered