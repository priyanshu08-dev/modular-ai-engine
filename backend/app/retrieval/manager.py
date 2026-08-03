from app.retrieval.exceptions import EmptyQueryError
from app.retrieval.models import RetrievalRequest, RetrievalResult
from app.retrieval.strategies.base import BaseRetrievalStrategy
from app.retrieval.strategies.vector_search import VectorSearchStrategy


class RetrievalManager:
    """
    Coordinates semantic retrieval workflows.
    """

    def __init__(
        self,
        strategy: BaseRetrievalStrategy | None = None,
    ) -> None:
        self._strategy = strategy or VectorSearchStrategy()

    async def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0,
        document_id: str | None = None,
    ) -> RetrievalResult:
        """
        Validates query inputs and delegates search execution to configured strategy.
        """
        clean_query = query.strip()
        if not clean_query:
            raise EmptyQueryError("Search query cannot be empty.")

        request = RetrievalRequest(
            query=clean_query,
            top_k=top_k,
            score_threshold=score_threshold,
            document_id=document_id,
        )

        return await self._strategy.retrieve(request)
