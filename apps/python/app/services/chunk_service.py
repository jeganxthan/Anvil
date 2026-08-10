from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chunk import Chunk
from app.db.schemas.chunk import ChunkCreate
from app.repository.chunk_repo import ChunkRepository


class ChunkService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ChunkRepository(session)

    async def create(
        self,
        data: ChunkCreate,
    ) -> Chunk:
        chunk = await self.repository.create(data)

        await self.session.commit()

        return chunk

    async def get(
        self,
        chunk_id: int,
    ) -> Chunk | None:
        return await self.repository.get(chunk_id)

    async def get_by_document(
        self,
        document_id: int,
    ) -> list[Chunk]:
        return await self.repository.get_by_document(
            document_id,
        )

    async def get_by_document_and_index(
        self,
        document_id: int,
        chunk_index: int,
    ) -> Chunk | None:
        return await self.repository.get_by_document_and_index(
            document_id,
            chunk_index,
        )

    async def delete(
        self,
        chunk_id: int,
    ) -> bool:
        chunk = await self.repository.get(chunk_id)

        if chunk is None:
            return False

        await self.repository.delete(chunk)

        await self.session.commit()

        return True

    async def delete_by_document(
        self,
        document_id: int,
    ) -> None:
        await self.repository.delete_by_document(
            document_id,
        )

        await self.session.commit()