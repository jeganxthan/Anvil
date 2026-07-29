from enum import StrEnum


class Provider(StrEnum):
    OPENAI = "openai"
    NVIDIA = "nvidia"
    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"

class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
