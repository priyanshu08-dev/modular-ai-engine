from app.chunking.models import ChunkingResult
from app.embeddings.factory import EmbeddingFactory
from app.embeddings.models import EmbeddingResult


class EmbeddingManager:
    """
    Coordinates embedding generation for documents and search queries.
    """

    async def generate_embeddings(
        self,
        chunking_result: ChunkingResult,
    ) -> EmbeddingResult:
        provider = EmbeddingFactory.get_provider()
        return await provider.generate_embeddings(chunking_result)

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:
        provider = EmbeddingFactory.get_provider()
        return await provider.embed_query(query)
