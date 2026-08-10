from fastapi import FastAPI

from app.api.routers import prompt_router
from app.middleware.process_time import log_request
from app.core.lifespan import lifespan

from app.core.exception_handler import register_exception_handlers

from app.api.routers.settings_router import router as settings_router

app = FastAPI(lifespan=lifespan)
app.include_router(settings_router)
app.include_router(prompt_router.router)
app.middleware("http")(log_request)
register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
