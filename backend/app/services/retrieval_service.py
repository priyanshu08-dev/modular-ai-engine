from app.retrieval.manager import RetrievalManager
from app.retrieval.models import RetrievalResult


class RetrievalService:
    """
    Application service coordinating retrieval queries.
    """

    def __init__(self) -> None:
        self._retrieval_manager = RetrievalManager()

    async def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0,
        document_id: str | None = None,
    ) -> RetrievalResult:
        return await self._retrieval_manager.search(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold,
            document_id=document_id,
        )
