from app.ai.context.model import ContextDocument


class ContextRanker:

    def rank(
        self,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:

        scored_documents = [
            document
            for document in documents
            if document.score is not None
        ]

        unscored_documents = [
            document
            for document in documents
            if document.score is None
        ]

        scored_documents.sort(
            key=lambda document: document.score,
            reverse=True,
        )

        return [
            *scored_documents,
            *unscored_documents,
        ]