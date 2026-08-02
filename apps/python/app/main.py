from fastapi import FastAPI

from app.api.routers import conversation_router, message_router
from app.middleware.process_time import log_request
from app.core.lifespan import lifespan
from app.api.routers import (nvidia)

from app.core.exception_handler import register_exception_handlers

app = FastAPI(lifespan=lifespan)
app.include_router(nvidia.router)
app.include_router(conversation_router.router)
app.include_router(message_router.router)
app.middleware("http")(log_request)
register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
