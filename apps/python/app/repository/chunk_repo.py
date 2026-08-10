from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chunk import Chunk
from app.db.schemas.chunk import ChunkCreate


class ChunkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data: ChunkCreate,
    ) -> Chunk:
        chunk = Chunk(
            document_id=data.document_id,
            content=data.content,
            chunk_index=data.chunk_index,
            metadata=data.metadata,
        )

        self.session.add(chunk)

        await self.session.flush()
        await self.session.refresh(chunk)

        return chunk

    async def get(
        self,
        chunk_id: int,
    ) -> Chunk | None:
        return await self.session.get(
            Chunk,
            chunk_id,
        )

    async def get_by_document(
        self,
        document_id: int,
    ) -> list[Chunk]:
        result = await self.session.execute(
            select(Chunk)
            .where(
                Chunk.document_id == document_id,
            )
            .order_by(
                Chunk.chunk_index,
            )
        )

        return list(result.scalars().all())

    async def get_by_document_and_index(
        self,
        document_id: int,
        chunk_index: int,
    ) -> Chunk | None:
        result = await self.session.execute(
            select(Chunk)
            .where(
                Chunk.document_id == document_id,
                Chunk.chunk_index == chunk_index,
            )
        )

        return result.scalar_one_or_none()
    
    async def create_many(
    self,
    data: list[ChunkCreate],
    ) -> list[Chunk]:
        chunks = [
            Chunk(
                document_id=item.document_id,
                content=item.content,
                chunk_index=item.chunk_index,
                metadata=item.metadata,
            )
            for item in data
        ]

        self.session.add_all(chunks)

        await self.session.flush()

        for chunk in chunks:
            await self.session.refresh(chunk)

        return chunks
    
    async def delete(
        self,
        chunk: Chunk,
    ) -> None:
        await self.session.delete(chunk)
        await self.session.flush()

    async def delete_by_document(
        self,
        document_id: int,
    ) -> None:
        await self.session.execute(
            delete(Chunk).where(
                Chunk.document_id == document_id,
            )
        )