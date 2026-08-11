from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VectorRecord:
    chunk_id: int
    content: str
    metadata: dict[str, Any]