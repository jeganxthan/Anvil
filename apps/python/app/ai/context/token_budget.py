from app.ai.context.model import ContextDocument


class ContextTokenBudget:

    def __init__(
        self,
        max_tokens: int,
    ):
        if max_tokens <= 0:
            raise ValueError(
                "max_tokens must be greater than 0",
            )

        self.max_tokens = max_tokens

    def apply(
        self,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:
        selected: list[ContextDocument] = []
        total_tokens = 0

        for document in documents:
            document_tokens = self._estimate_tokens(
                document.content,
            )

            if (
                total_tokens + document_tokens
                > self.max_tokens
            ):
                break

            selected.append(document)
            total_tokens += document_tokens

        return selected

    @staticmethod
    def _estimate_tokens(
        content: str,
    ) -> int:
        if not content:
            return 0

        # Simple approximation for now.
        return max(1, len(content) // 4)