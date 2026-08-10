from enum import Enum

class PromptType(str, Enum):
    SYSTEM = "system"
    RAG = "rag"
    TOOL = "tool"
    SUMMARY = "summary"