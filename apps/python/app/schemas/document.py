from pydantic import BaseModel


class DocumentCreate(BaseModel):
    name: str

    path: str

    mime_type: str

    size: int
    
