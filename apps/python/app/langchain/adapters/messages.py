from app.providers.schema.models import ChatMessage, GenerateResponse
from app.core.enum import MessageRole
from langchain_core.messages import(
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage
)
class MessageAdapter:
    @staticmethod
    def to_chat_messages(messages:list[BaseMessage])->list[ChatMessage]:
        converted: list[ChatMessage]=[]
        for message in messages:
            converted.append(
                ChatMessage(
                    role=MessageAdapter._to_role(message),
                    content=str(message.content),
                )
            )

        return converted
    
    @staticmethod
    def to_ai_message(response:GenerateResponse)->AIMessage:
        return AIMessage(
            content=response.content
        )
    
    @staticmethod
    def _to_role(message:BaseMessage)->MessageRole:
        if isinstance(message, HumanMessage):
            return MessageRole.USER
        if isinstance(message, AIMessage):
            return MessageRole.ASSISTANT

        if isinstance(message, SystemMessage):
            return MessageRole.SYSTEM

        if isinstance(message, ToolMessage):
            return MessageRole.TOOL

        raise ValueError(
            f"Unsupported message type: {type(message).__name__}"
        )