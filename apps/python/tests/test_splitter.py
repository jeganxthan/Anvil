from pathlib import Path

from app.langchain.documents.spliter.pipeline import SplitterPipeline
from app.langchain.documents.spliter.recursive import RecursiveSplitter
from app.langchain.documents.loaders.text import TXTLoader

loader = TXTLoader(
    Path("tests/sample.txt"),
)

documents = loader.load()

pipeline = SplitterPipeline()
pipeline.register(
    RecursiveSplitter(
        chunk_size=200,
        chunk_overlap=50,
    )
)

chunks = pipeline.split(documents)

print(f"Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print("=" * 80)
    print(i)
    print(chunk.page_content)