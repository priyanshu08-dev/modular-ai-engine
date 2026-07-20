from abc import ABC, abstractmethod

from app.chunking.models import ChunkingResult
from app.document.models import Document


class BaseChunkingStrategy(ABC):
    """
    Base interface for all chunking strategies.
    """

    @abstractmethod
    def split(
        self,
        document: Document,
    ) -> ChunkingResult:
        """
        Split a document into semantic chunks.
        """