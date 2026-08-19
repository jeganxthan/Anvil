from app.langchain.context.builder import ContextBuilder


def main():

    builder = ContextBuilder()

    messages = builder.build(
        system_prompt=(
            "You are Anvil, an AI assistant. "
            "Answer accurately and concisely."
        ),
        memories=[
            "The user is building a RAG application.",
            "The user uses SQLite-Vec for vector storage.",
        ],
        documents=[
            (
                "RAG combines retrieval with generation "
                "to provide external knowledge to an LLM."
            ),
            (
                "SQLite-Vec stores embeddings and supports "
                "vector similarity search."
            ),
        ],
        conversation=[
            {
                "role": "user",
                "content": "I'm building an AI application.",
            },
            {
                "role": "assistant",
                "content": "That's great. What part are you working on?",
            },
        ],
        query="What vector database am I using?",
    )

    for index, message in enumerate(messages):

        print(f"\n--- Message {index + 1} ---")
        print(f"type: {type(message).__name__}")
        print(f"content:\n{message.content}")


if __name__ == "__main__":
    main()