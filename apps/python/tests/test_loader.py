from app.langchain.documents.loaders.text import TXTLoader
from pathlib import Path

loader = TXTLoader(
    Path("tests/sample.txt")
)

documents = loader.load()

print(len(documents))
print(documents[0].page_content)
print(documents[0].metadata)