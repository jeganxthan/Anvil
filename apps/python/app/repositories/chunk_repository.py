from collections.abc import Sequence
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.vectorstore.model import ChunkCreate
from app.db.models.chunk import Chunk

class ChunkRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        
    async def create(self,data:ChunkCreate)->Chunk:
        chunk = Chunk(
            document_id=data.document_id,
            content=data.content,
            chunk_index=data.chunk_index,
            metadata=data.metadata
        )
        self.session.add(chunk)

        await self.session.flush()
        await self.session.refresh(chunk)
        return chunk
    
    async def create_many(
        self, data:Sequence[ChunkCreate]
    )->list[Chunk]:
        chunks=[
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

    async def get(
        self,
        chunk_id: int,
    ) -> Chunk | None:
        return await self.session.get(
            Chunk,
            chunk_id,
        )

    async def get_many(
        self,
        chunk_ids: Sequence[int],
    ) -> list[Chunk]:
        if not chunk_ids:
            return []

        stmt = (
            select(Chunk)
            .where(
                Chunk.id.in_(chunk_ids)
            )
        )

        result = await self.session.execute(stmt)

        chunks = list(result.scalars().all())

        chunk_map = {
            chunk.id: chunk
            for chunk in chunks
        }

        return [
            chunk_map[chunk_id]
            for chunk_id in chunk_ids
            if chunk_id in chunk_map
        ]
    
    async def list(
        self,
        document_id: int,
    ) -> list[Chunk]:
        stmt = (
            select(Chunk)
            .where(
                Chunk.document_id == document_id
            )
            .order_by(
                Chunk.chunk_index
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
    
    async def update_metadata(
        self,
        chunk_id: int,
        metadata: dict[str, object],
    ) -> Chunk | None:
        chunk = await self.get(chunk_id)

        if chunk is None:
            return None

        chunk.metadata = metadata

        await self.session.flush()
        await self.session.refresh(chunk)

        return chunk

    async def delete(
        self,
        chunk_id: int,
    ) -> None:
        chunk = await self.get(chunk_id)

        if chunk is None:
            return

        await self.session.delete(chunk)

        await self.session.flush()

    async def delete_by_document(
        self,
        document_id: int,
    ) -> None:
        await self.session.execute(
            delete(Chunk).where(
                Chunk.document_id == document_id
            )
        )

        await self.session.flush()