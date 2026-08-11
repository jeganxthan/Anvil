from pydantic import BaseModel


class IngestionRequest(BaseModel):
    path: str
    name: str
    mime_type: str
    size: int