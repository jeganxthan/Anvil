from fastapi import FastAPI
from app.router import nvidia
app = FastAPI()
app.include_router(nvidia.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}