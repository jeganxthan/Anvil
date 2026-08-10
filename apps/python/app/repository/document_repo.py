from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.db.schemas.document import DocumentCreate


class DocumentRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        data: DocumentCreate,
    ) -> Document:
        document = Document(
            name=data.name,
            path=data.path,
            mime_type=data.mime_type,
            size=data.size,
        )

        self.session.add(document)

        await self.session.flush()
        await self.session.refresh(document)

        return document

    async def get(
        self,
        document_id: int,
    ) -> Document | None:
        return await self.session.get(
            Document,
            document_id,
        )

    async def get_by_path(
        self,
        path: str,
    ) -> Document | None:
        result = await self.session.execute(
            select(Document).where(
                Document.path == path,
            )
        )

        return result.scalar_one_or_none()