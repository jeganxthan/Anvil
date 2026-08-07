
from app.langchain.documents.spliter.pipeline import SplitterPipeline

from app.langchain.ingestion.models import (
    IngestionRequest,
    IngestionResponse,
)
from app.langchain.vectorstores.sqlite_vec import AnvilSQLiteVec
from app.langchain.documents.loaders.registry import LoaderRegistry
from app.langchain.documents.transformer.pipeline import DocumentTransformerPipeline


class IngestionPipeline:
    def __init__(
        self,
        loader_registry: LoaderRegistry,
        transformer_pipeline: DocumentTransformerPipeline,
        splitter_pipeline: SplitterPipeline,
        vectorstore: AnvilSQLiteVec,
    ):
        self.loader_registry = loader_registry
        self.transformer_pipeline = transformer_pipeline
        self.splitter_pipeline = splitter_pipeline
        self.vectorstore = vectorstore

    async def ingest(
        self,
        request: IngestionRequest,
    ) -> IngestionResponse:
        #
        # Resolve loader
        #
        loader = self.loader_registry.resolve(
            request.path,
        )

        #
        # Load document(s)
        #
        documents = loader.load()

        #
        # Transform
        #
        documents = self.transformer_pipeline.transform(
            documents,
        )

        #
        # Split
        #
        documents = self.splitter_pipeline.split(
            documents,
        )

        #
        # Store in vector store
        #
        ids = await self.vectorstore.add_documents(
            documents,
            document_id=request.document_id,
        )

        return IngestionResponse(
            documents=len(documents),
            chunks=len(ids),
        )