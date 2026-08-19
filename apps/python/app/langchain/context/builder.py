from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)


class ContextBuilder:

    def build(
        self,
        system_prompt: str,
        memories: list[str] | None = None,
        documents: list[str] | None = None,
        conversation: list[dict[str, str]] | None = None,
        query: str = "",
    ) -> list[BaseMessage]:

        messages: list[BaseMessage] = []

        # 1. System instructions
        messages.append(
            SystemMessage(
                content=system_prompt,
            ),
        )

        # 2. Long-term / user memory
        if memories:

            memory_context = "\n".join(
                f"- {memory}"
                for memory in memories
            )

            messages.append(
                SystemMessage(
                    content=(
                        "Relevant user memory:\n"
                        f"{memory_context}"
                    ),
                ),
            )

        # 3. RAG context
        if documents:

            document_context = "\n\n".join(
                f"[Document {index + 1}]\n{document}"
                for index, document in enumerate(documents)
            )

            messages.append(
                SystemMessage(
                    content=(
                        "Relevant knowledge from "
                        "retrieved documents:\n\n"
                        f"{document_context}"
                    ),
                ),
            )

        # 4. Previous conversation
        if conversation:

            for message in conversation:

                role = message["role"]
                content = message["content"]

                if role == "user":

                    messages.append(
                        HumanMessage(
                            content=content,
                        ),
                    )

                elif role == "assistant":

                    messages.append(
                        AIMessage(
                            content=content,
                        ),
                    )

        # 5. Current user query
        if query:

            messages.append(
                HumanMessage(
                    content=query,
                ),
            )

        return messages