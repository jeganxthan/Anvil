from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.factory import EmbeddingFactory


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

    vector = embeddings.embed_query(
        "What is artificial intelligence?",
    )

    print("Dimension:", len(vector))
    print("Embedding:", vector)


if __name__ == "__main__":
    main()