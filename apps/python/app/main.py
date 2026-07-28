from fastapi import FastAPI

from app.middleware.process_time import log_request
from app.core.lifespan import lifespan
from app.router import nvidia

from app.core.exceptions import AppException
from app.core.exception_handler import register_exception_handlers

app = FastAPI(lifespan=lifespan)
app.include_router(nvidia.router)
app.middleware("http")(log_request)
register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
