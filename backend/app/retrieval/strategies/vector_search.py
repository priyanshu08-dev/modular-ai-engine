from app.config.settings import settings
from app.embeddings.manager import EmbeddingManager
from app.retrieval.exceptions import SearchExecutionError
from app.retrieval.mapper import RetrievalMapper
from app.retrieval.models import RetrievalRequest, RetrievalResult
from app.retrieval.strategies.base import BaseRetrievalStrategy
from app.vectorstore.factory import VectorStoreFactory


class VectorSearchStrategy(BaseRetrievalStrategy):
    """
    Standard dense vector similarity retrieval strategy.
    """

    def __init__(self) -> None:
        self._embedding_manager = EmbeddingManager()
        self._vectorstore_provider = VectorStoreFactory.get_provider()
        self._collection_name = settings.DEFAULT_VECTOR_COLLECTION

    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:
        """
        Embeds query string, performs vector DB search, maps and filters results.
        """
        try:
            query_vector = await self._embedding_manager.embed_query(
                request.query
            )

            raw_response = await self._vectorstore_provider.similarity_search(
                collection_name=self._collection_name,
                query_embedding=query_vector,
                limit=request.top_k,
                where={"document_id": request.document_id} if request.document_id else None,
            )

            chunks = RetrievalMapper.from_chroma_response(
                raw_response=raw_response,
                score_threshold=request.score_threshold,
            )

            if request.document_id:
                chunks = [
                    chunk for chunk in chunks
                    if chunk.document_id == request.document_id
                ]

            return RetrievalResult(
                query=request.query,
                chunks=chunks,
                strategy_name=self.__class__.__name__,
            )

        except Exception as exc:
            raise SearchExecutionError(
                f"Vector retrieval failed for query: '{request.query}'"
            ) from exc
