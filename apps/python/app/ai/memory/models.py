from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MemoryMessage:
    role: str
    content: str
    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )