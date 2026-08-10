from sqlalchemy import delete, exists, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.schemas.document import DocumentCreate


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
        stmt = select(Document).where(
            Document.path == path,
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def exists(
        self,
        path: str,
    ) -> bool:
        stmt = select(
            exists().where(
                Document.path == path,
            )
        )

        result = await self.session.execute(stmt)

        return bool(result.scalar())

    async def list_all(
        self,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .order_by(Document.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def delete(
        self,
        document_id: int,
    ) -> None:
        await self.session.execute(
            delete(Document).where(
                Document.id == document_id,
            )
        )

        await self.session.flush()
        
    async def update(
        self,
        document: Document,
    ) -> Document:
        await self.session.flush()
        await self.session.refresh(document)

        return document
    

    async def count(
        self,
    ) -> int:
        stmt = select(func.count()).select_from(
            Document
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()
    
    async def delete_by_path(
    self,
    path: str,
) -> None:
        await self.session.execute(
            delete(Document).where(
                Document.path == path,
            )
        )

        await self.session.flush()