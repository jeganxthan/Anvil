from app.ai.context.model import ContextDocument


class ContextDeduplicator:

    def deduplicate(
        self,
        documents: list[ContextDocument],
    ) -> list[ContextDocument]:

        seen: set[str] = set()
        unique_documents: list[ContextDocument] = []

        for document in documents:
            content = document.content.strip()

            if not content:
                continue

            if content in seen:
                continue

            seen.add(content)
            unique_documents.append(document)

        return unique_documents