from app.ai.context.model import Context, ContextDocument, ContextMessage


class ContextBuilder:

    def build(
        self,
        query: str,
        documents: list[ContextDocument] | None = None,
        messages: list[ContextMessage] | None = None,
    ) -> Context:
        return Context(
            query=query,
            documents=documents or [],
            messages=messages or [],
        )