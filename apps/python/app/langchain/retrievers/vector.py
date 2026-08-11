from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from app.langchain.vectorstore.sqlite_vec import AnvilSQLiteVec


class VectorRetriever(BaseRetriever):
    vectorstore: AnvilSQLiteVec
    k: int = 5

    def _get_relevant_documents(
        self,
        query: str,
    ) -> list[Document]:
        return self.vectorstore.similarity_search(
            query,
            k=self.k,
        )