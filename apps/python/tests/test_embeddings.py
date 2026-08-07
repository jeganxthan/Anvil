from app.langchain.embeddings.default import DefaultEmbeddings

embeddings = DefaultEmbeddings()

vectors = embeddings.embed_documents(
    [
        "Hello world",
        "LangChain is awesome",
    ]
)

print(len(vectors))
print(len(vectors[0]))