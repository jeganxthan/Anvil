import asyncio

from app.ai.memory.manager import MemoryManager
from app.ai.memory.models import MemoryMessage
from app.ai.memory.short_term import ShortTermMemory


async def main():

    memory = MemoryManager(
        short_term=ShortTermMemory(
            max_messages=2,
        ),
    )

    session_id = "test-session"

    await memory.add_message(
        session_id,
        MemoryMessage(
            role="user",
            content="What is RAG?",
        ),
    )

    await memory.add_message(
        session_id,
        MemoryMessage(
            role="assistant",
            content="RAG means Retrieval-Augmented Generation.",
        ),
    )

    await memory.add_message(
        session_id,
        MemoryMessage(
            role="user",
            content="What is retrieval?",
        ),
    )

    await memory.add_message(
        session_id,
        MemoryMessage(
            role="assistant",
            content="Retrieval finds relevant information.",
        ),
    )

    messages = await memory.get_messages(
        session_id,
    )

    for message in messages:
        print(
            f"{message.role}: {message.content}"
        )


if __name__ == "__main__":
    asyncio.run(main())