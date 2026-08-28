from app.ai.memory.models import MemoryMessage


class ShortTermMemory:

    def __init__(
        self,
        max_messages: int = 20,
    ):
        if max_messages <= 0:
            raise ValueError(
                "max_messages must be greater than 0",
            )

        self.max_messages = max_messages

        self._sessions: dict[
            str,
            list[MemoryMessage],
        ] = {}

    async def add(
        self,
        session_id: str,
        message: MemoryMessage,
    ) -> None:

        messages = self._sessions.setdefault(
            session_id,
            [],
        )

        messages.append(message)

        if len(messages) > self.max_messages:
            del messages[
                : len(messages) - self.max_messages
            ]

    async def add_user_message(
        self,
        session_id: str,
        content: str,
    ) -> None:

        await self.add(
            session_id,
            MemoryMessage(
                role="user",
                content=content,
            ),
        )

    async def add_assistant_message(
        self,
        session_id: str,
        content: str,
    ) -> None:

        await self.add(
            session_id,
            MemoryMessage(
                role="assistant",
                content=content,
            ),
        )

    async def get(
        self,
        session_id: str,
    ) -> list[MemoryMessage]:

        return list(
            self._sessions.get(
                session_id,
                [],
            )
        )

    async def clear(
        self,
        session_id: str,
    ) -> None:

        self._sessions.pop(
            session_id,
            None,
        )

    async def count(
        self,
        session_id: str,
    ) -> int:

        return len(
            self._sessions.get(
                session_id,
                [],
            )
        )