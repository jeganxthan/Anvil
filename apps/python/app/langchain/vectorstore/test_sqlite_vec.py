from langchain_core.documents import Document

from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.factory import EmbeddingFactory
from app.langchain.vectorstore.sqlite_vec import AnvilSQLiteVec
from app.core.settings import settings


def main():
    config = EmbeddingModel(
        provider="huggingface",
        model="BAAI/bge-small-en-v1.5",
        dimension=384,
        device="cpu",
        normalize=True,
        batch_size=32,
        is_active=True,
    )

    embeddings = EmbeddingFactory.create(
        config,
    )

    vectorstore = AnvilSQLiteVec(
        db_path=settings.sqlite_vec_path,
        embedding=embeddings,
    )

    documents = [
        Document(
            page_content=(
                "Artificial intelligence is the field "
                "of building systems that perform tasks "
                "that normally require human intelligence."
            ),
            metadata={
                "source": "test",
                "topic": "ai",
            },
            id="1",
        ),
        Document(
            page_content=(
                "Machine learning allows computers "
                "to learn patterns from data."
            ),
            metadata={
                "source": "test",
                "topic": "machine-learning",
            },
            id="2",
        ),
        Document(
            page_content=(
                "Linux is an operating system kernel."
            ),
            metadata={
                "source": "test",
                "topic": "linux",
            },
            id="3",
        ),
    ]

    vectorstore.add_documents(
        documents,
    )

    results = vectorstore.similarity_search_with_score(
        "What is artificial intelligence?",
        k=2,
    )

    for document, score in results:
        print("Score:", score)
        print("Content:", document.page_content)
        print("Metadata:", document.metadata)
        print("---")


if __name__ == "__main__":
    main()