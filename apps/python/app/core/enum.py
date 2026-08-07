from enum import StrEnum



class Provider(StrEnum):
    LITELLM = "litellm"

class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class EmbeddingProvider(StrEnum):
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    OLLAMA = "ollama"
    OPENAI = "openai"
    FASTEMBED = "fastembed"
    VOYAGE = "voyage"
    
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