from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.vector_record import VectorRecord


class VectorRecordRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create_many(
        self,
        chunk_ids: list[int],
        embedding_model_id: int,
    ) -> list[VectorRecord]:

        if not chunk_ids:
            return []

        records = [
            VectorRecord(
                chunk_id=chunk_id,
                embedding_model_id=embedding_model_id,
            )
            for chunk_id in chunk_ids
        ]

        self.session.add_all(records)

        await self.session.flush()

        return records

    async def exists_for_model(
        self,
        embedding_model_id: int,
    ) -> bool:

        result = await self.session.execute(
            select(VectorRecord.id)
            .where(
                VectorRecord.embedding_model_id
                == embedding_model_id,
            )
            .limit(1),
        )

        return result.scalar_one_or_none() is not None

    async def exists_for_chunk(
        self,
        chunk_id: int,
        embedding_model_id: int,
    ) -> bool:

        result = await self.session.execute(
            select(VectorRecord.id)
            .where(
                VectorRecord.chunk_id == chunk_id,
                VectorRecord.embedding_model_id
                == embedding_model_id,
            )
            .limit(1),
        )

        return result.scalar_one_or_none() is not None

    async def get_chunk_ids(
        self,
        embedding_model_id: int,
    ) -> list[int]:

        result = await self.session.execute(
            select(VectorRecord.chunk_id)
            .where(
                VectorRecord.embedding_model_id
                == embedding_model_id,
            )
            .order_by(
                VectorRecord.chunk_id,
            ),
        )

        return list(result.scalars().all())

    async def delete_for_model(
        self,
        embedding_model_id: int,
    ) -> None:

        await self.session.execute(
            delete(VectorRecord).where(
                VectorRecord.embedding_model_id
                == embedding_model_id,
            ),
        )

        await self.session.flush()