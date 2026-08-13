import re
from abc import ABC, abstractmethod
from app.ai.context.model import ContextDocument



class ContextCompressor(ABC):

    @abstractmethod
    def compress(
        self,
        query: str,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:
        ...


class NoOpCompressor(ContextCompressor):

    def compress(
        self,
        query: str,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:
        return documents


class ExtractiveCompressor(ContextCompressor):

    def __init__(
        self,
        max_tokens_per_document: int = 500,
    ):
        if max_tokens_per_document <= 0:
            raise ValueError(
                "max_tokens_per_document must be greater than 0",
            )

        self.max_tokens_per_document = (
            max_tokens_per_document
        )

    def compress(
        self,
        query: str,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:

        query_terms = self._terms(query)

        result: list[ContextDocument] = []

        for document in documents:
            sentences = self._split_sentences(
                document.content,
            )

            ranked = sorted(
                sentences,
                key=lambda sentence: self._relevance(
                    sentence,
                    query_terms,
                ),
                reverse=True,
            )

            selected: list[str] = []
            token_count = 0

            for sentence in ranked:
                sentence_tokens = self._estimate_tokens(
                    sentence,
                )

                if (
                    token_count + sentence_tokens
                    > self.max_tokens_per_document
                ):
                    continue

                selected.append(sentence)
                token_count += sentence_tokens

            if not selected:
                continue

            selected_set = set(selected)

            # Preserve the original document order.
            compressed_content = " ".join(
                sentence
                for sentence in sentences
                if sentence in selected_set
            )

            result.append(
                ContextDocument(
                    content=compressed_content,
                    metadata=document.metadata,
                    score=document.score,
                )
            )

        return result

    @staticmethod
    def _terms(text: str) -> set[str]:
        return {
            word.lower()
            for word in re.findall(
                r"\b\w+\b",
                text,
            )
            if len(word) > 2
        }

    @classmethod
    def _relevance(
        cls,
        sentence: str,
        query_terms: set[str],
    ) -> int:
        sentence_terms = cls._terms(sentence)

        return len(
            sentence_terms & query_terms,
        )

    @staticmethod
    def _split_sentences(
        content: str,
    ) -> list[str]:
        return [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+|\n+",
                content,
            )
            if sentence.strip()
        ]

    @staticmethod
    def _estimate_tokens(
        content: str,
    ) -> int:
        return max(
            1,
            len(content) // 4,
        )