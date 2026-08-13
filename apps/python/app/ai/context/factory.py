from app.ai.context.builder import ContextBuilder
from app.ai.context.compressor import ExtractiveCompressor
from app.ai.context.deduplicator import ContextDeduplicator
from app.ai.context.filter import ContextFilter
from app.ai.context.ordering import PreserveOrder
from app.ai.context.pipeline import ContextPipeline
from app.ai.context.ranker import ContextRanker
from app.ai.context.token_budget import ContextTokenBudget


def create_context_pipeline() -> ContextPipeline:

    return ContextPipeline(
        context_filter=ContextFilter(),
        deduplicator=ContextDeduplicator(),
        ranker=ContextRanker(),
        token_budget=ContextTokenBudget(
            max_tokens=3000,
        ),
        compressor=ExtractiveCompressor(
            max_tokens_per_document=500,
        ),
        ordering=PreserveOrder(),
        builder=ContextBuilder(),
    )