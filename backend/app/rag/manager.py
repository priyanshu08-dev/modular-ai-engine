from app.rag.formatter import ContextFormatter
from app.rag.models import RAGContext
from app.retrieval.manager import RetrievalManager


class RAGManager:
    """
    Coordinates semantic document retrieval and context formatting
    for Retrieval-Augmented Generation workflows.
    """

    def __init__(
        self,
        retrieval_manager: RetrievalManager | None = None,
    ) -> None:
        self._retrieval_manager = retrieval_manager or RetrievalManager()

    async def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.2,
        document_id: str | None = None,
    ) -> RAGContext:
        """
        Executes semantic search over stored vector collections and returns a RAGContext object.
        """
        retrieval_result = await self._retrieval_manager.search(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold,
            document_id=document_id,
        )

        return ContextFormatter.format_chunks(
            query=query,
            chunks=retrieval_result.chunks,
        )
