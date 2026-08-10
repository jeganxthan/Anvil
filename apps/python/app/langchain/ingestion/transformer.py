from langchain_core.documents import Document


class DocumentTransformer:

    async def transform(
        self,
        documents: list[Document],
    ) -> list[Document]:

        transformed = []

        for document in documents:
            content = document.page_content.strip()

            if not content:
                continue

            transformed.append(
                Document(
                    page_content=content,
                    metadata=document.metadata,
                )
            )

        return transformed