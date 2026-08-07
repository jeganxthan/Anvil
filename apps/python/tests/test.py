from app.langchain.documents.loaders.text import TXTLoader

loader = TXTLoader("sample.txt")

documents = loader.load()

print(len(documents))
print(documents[0].page_content)
print(documents[0].metadata)