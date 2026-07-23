from __future__ import annotations

from abc import ABC, abstractmethod

from app.chunking.models import ChunkingResult
from app.embeddings.models import EmbeddingResult


class BaseEmbeddingProvider(ABC):
    """
    Base interface implemented by all embedding providers.
    """

    @abstractmethod
    async def generate_embeddings(
        self,
        chunking_result: ChunkingResult,
    ) -> EmbeddingResult:
        """
        Generate embeddings for every chunk contained in the
        supplied ChunkingResult.
        """
        pass