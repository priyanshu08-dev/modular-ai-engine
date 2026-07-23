from app.chunking.models import ChunkingResult

from app.embeddings.factory import EmbeddingFactory
from app.embeddings.models import EmbeddingResult


class EmbeddingManager:
    """
    Coordinates embedding generation.
    """

    async def generate_embeddings(
        self,
        chunking_result: ChunkingResult,
    ) -> EmbeddingResult:
        provider = EmbeddingFactory.get_provider()

        return await provider.generate_embeddings(chunking_result)
