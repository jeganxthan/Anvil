from langchain_core.messages import BaseMessage

from app.ai.memory.manager import MemoryManager
from app.langchain.retrieval.retriever import VectorRetriever

from app.langchain.context.builder import ContextBuilder


class ContextService:

    def __init__(
        self,
        memory_manager: MemoryManager,
        retriever: VectorRetriever,
        builder: ContextBuilder,
    ):
        self.memory_manager = memory_manager
        self.retriever = retriever
        self.builder = builder

    async def build(
        self,
        session_id: str,
        query: str,
        system_prompt: str,
        conversation: list[dict[str, str]] | None = None,
    ) -> list[BaseMessage]:

        # -----------------------------------------
        # 1. Get short-term conversation memory
        # -----------------------------------------

        messages = await self.memory_manager.get_messages(
            session_id,
        )

        memories = [
            message.content
            for message in messages
        ]

        # -----------------------------------------
        # 2. Retrieve relevant documents
        # -----------------------------------------

        documents = await self.retriever.retrieve(
            query,
        )

        document_contents = [
            document.page_content
            for document in documents
        ]

        # -----------------------------------------
        # 3. Build final context
        # -----------------------------------------

        return self.builder.build(
            system_prompt=system_prompt,
            memories=memories,
            documents=document_contents,
            conversation=conversation,
            query=query,
        )