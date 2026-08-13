from app.ai.context.builder import ContextBuilder
from app.ai.context.compressor import ContextCompressor
from app.ai.context.deduplicator import ContextDeduplicator
from app.ai.context.filter import ContextFilter
from app.ai.context.ordering import ContextOrdering
from app.ai.context.ranker import ContextRanker
from app.ai.context.token_budget import ContextTokenBudget
from app.ai.context.model import Context, ContextDocument, ContextMessage


class ContextPipeline:

    def __init__(
        self,
        context_filter: ContextFilter,
        deduplicator: ContextDeduplicator,
        ranker: ContextRanker,
        token_budget: ContextTokenBudget,
        compressor: ContextCompressor,
        ordering: ContextOrdering,
        builder: ContextBuilder,
    ):
        self.context_filter = context_filter
        self.deduplicator = deduplicator
        self.ranker = ranker
        self.token_budget = token_budget
        self.compressor = compressor
        self.ordering = ordering
        self.builder = builder

    def run(
        self,
        query: str,
        documents: list[ContextDocument],
        messages: list[ContextMessage]|None=None
    ) -> Context:

        # 1. Filter
        documents = self.context_filter.filter(
            documents,
        )

        # 2. Deduplicate
        documents = self.deduplicator.deduplicate(
            documents,
        )

        # 3. Rank
        documents = self.ranker.rank(
            documents,
        )

        # 4. Token budget
        documents = self.token_budget.apply(
            documents,
        )

        # 5. Compress
        documents = self.compressor.compress(
            query=query,
            documents=documents,
        )

        # 6. Order
        documents = self.ordering.order(
            documents,
        )

        # 7. Build final context
        return self.builder.build(
            query=query,
            documents=documents,
            messages=messages or [],
        )