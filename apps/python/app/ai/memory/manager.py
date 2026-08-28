from app.ai.memory.manager import ShortTermMemory
import app.ai.memory.models


class MemoryManager:

    def __init__(
        self,
        short_term: ShortTermMemory,
    ):
        self.short_term = short_term

    async def add_message(
        self,
        session_id: str,
        message: MemoryMessage,
    ) -> None:

        await self.short_term.add(
            session_id,
            message,
        )

    async def get_messages(
        self,
        session_id: str,
    ) -> list[MemoryMessage]:

        return await self.short_term.get(
            session_id,
        )

    async def clear(
        self,
        session_id: str,
    ) -> None:

        await self.short_term.clear(
            session_id,
        )