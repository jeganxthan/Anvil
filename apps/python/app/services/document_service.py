from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.db.schemas.document import DocumentCreate
from app.repository.document_repo import DocumentRepository


class DocumentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = DocumentRepository(session)

    async def create(
        self,
        data: DocumentCreate,
    ) -> Document:
        # Prevent duplicate documents with the same path
        existing = await self.repository.get_by_path(
            data.path
        )

        if existing is not None:
            raise ValueError(
                f"Document already exists at path: {data.path}"
            )

        document = await self.repository.create(data)

        await self.session.commit()

        return document

    async def get(
        self,
        document_id: int,
    ) -> Document | None:
        return await self.repository.get(document_id)

    async def get_by_path(
        self,
        path: str,
    ) -> Document | None:
        return await self.repository.get_by_path(path)
