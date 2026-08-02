from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession 
from app.core.exceptions import ConversationNotFound
from app.providers.registry import ProviderRegistry
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import ChatGenerateRequest
from app.providers.schema.models import GenerateRequest, GenerateResponse
from app.core.enum import MessageRole
from app.db.models.message import Message
from app.ai.builders.conversation_request_builder import ConversationRequestBuilder
from app.db.models.conversation import Conversation

class ChatService:
    def __init__(self, session:AsyncSession, provider_registry: ProviderRegistry, builders: ConversationRequestBuilder):
        self.session = session
        self.provider_registry = provider_registry
        self.conversation_repo=ConversationRepository(session)
        self.message_repo=MessageRepository(session)
        self.builders=builders
        
    async def _prepare_generate_request(
        self,
        request: ChatGenerateRequest,
    ) -> tuple[Conversation, GenerateRequest]:
        conversation = await self.conversation_repo.get_by_id(
            request.conversation_id
        )

        if conversation is None:
            raise ConversationNotFound()

        user_position = await self.message_repo.next_position(
            conversation.id
        )

        user_message = Message.from_create(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.content,
            position=user_position,
        )

        await self.message_repo.create(user_message)

        history = await self.message_repo.list(
            conversation.id
        )

        generate_request = self.builders.build(
            conversation=conversation,
            messages=history,
        )

        return conversation, generate_request
    
    async def generate(
    self,
        request: ChatGenerateRequest,
    ) -> GenerateResponse:
        try:
            conversation, generate_request = await self._prepare_generate_request(
                request
            )
    
            provider = self.provider_registry.get(conversation.provider)
    
            response = await provider.generate(generate_request)
    
            assistant_position = await self.message_repo.next_position(
                conversation.id
            )
    
            assistant_message = Message.from_create(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT,
                content=response.content,
                position=assistant_position,
            )
    
            await self.message_repo.create(assistant_message)
            await self.session.commit()
    
            return response
    
        except Exception:
            await self.session.rollback()
            raise
    
    async def generate_stream(
    self,
    request: ChatGenerateRequest,
) -> AsyncIterator[str]:
     try:
         conversation, generate_request = await self._prepare_generate_request(
             request
         )
    
         provider = self.provider_registry.get(conversation.provider)
    
         chunks: list[str] = []
    
         async for chunk in provider.generate_stream(generate_request):
             chunks.append(chunk)
             yield chunk
    
         assistant_position = await self.message_repo.next_position(
             conversation.id
         )
    
         assistant_message = Message.from_create(
             conversation_id=conversation.id,
             role=MessageRole.ASSISTANT,
             content="".join(chunks),
             position=assistant_position,
         )
    
         await self.message_repo.create(assistant_message)
         await self.session.commit()
    
     except Exception:
         await self.session.rollback()
         raise