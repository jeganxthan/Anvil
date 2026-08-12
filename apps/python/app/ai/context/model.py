from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextDocument:
    content: str
    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
    score: float | None = None


@dataclass
class ContextMessage:
    role: str
    content: str
    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass
class Context:
    query: str
    documents: list[ContextDocument] = field(
        default_factory=list,
    )
    messages: list[ContextMessage] = field(
        default_factory=list,
    )