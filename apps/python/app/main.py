from fastapi import FastAPI

app = FastAPI()
from app.routers.embedding_router import router as embedding_router
from app.routers.document_router import router as document_router
from app.routers.chunk_router import router as chunk_router

app.include_router(embedding_router)
app.include_router(document_router)
app.include_router(chunk_router)

@app.get("/")
async def root():
    return {"message": "Anvil"}


# uv run uvicorn app.main:app --reload