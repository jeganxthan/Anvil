from fastapi import FastAPI

app = FastAPI()
from app.routers.embedding_router import router as embedding_router
from app.routers.document_router import router as document_router
from app.routers.chunk_router import router as chunk_router
from app.routers.ingestion_router import router as ingestion_router
from app.routers.llm import router as llm
from app.routers.llm_models import router as llm_models_router

app.include_router(embedding_router)
app.include_router(document_router)
app.include_router(chunk_router)
app.include_router(ingestion_router)
app.include_router(llm)
app.include_router(llm_models_router)

@app.get("/")
async def root():
    return {"message": "Anvil"}


# uv run uvicorn app.main:app --reload
# cd ~/Desktop/Anvil/apps/python
# sqlite3 anvil.db