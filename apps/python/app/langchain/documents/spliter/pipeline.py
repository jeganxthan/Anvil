from langchain_core.documents import Document
from app.langchain.documents.spliter.base import BaseSplitter



class SplitterPipeline:
    def __init__(self):
        self.splitters: list[BaseSplitter] = []

    def register(
        self,
        splitter: BaseSplitter,
    ) -> None:
        self.splitters.append(splitter)

    async def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        for splitter in self.splitters:
            documents = await splitter.split(
                documents,
            )

        return documents