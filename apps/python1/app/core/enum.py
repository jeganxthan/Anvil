from enum import StrEnum




class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
    
class ChunkingStrategy(StrEnum):
    RECURSIVE = "recursive"
    TOKEN = "token"
    MARKDOWN = "markdown"
    SEMANTIC = "semantic"
    
class LoaderType(StrEnum):
    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"
    WEB = "web"
    
class EmbeddingProvider(StrEnum):
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"
    OLLAMA = "ollama"
    NVIDIA = "nvidia"