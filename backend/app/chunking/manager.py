from app.chunking.models import ChunkingResult
from app.chunking.strategies.base import BaseChunkingStrategy
from app.document.models import Document


class ChunkManager:
    """
    Coordinates document chunking.

    The manager knows nothing about
    LangChain implementations.
    """

    def __init__(
        self,
        strategy: BaseChunkingStrategy,
    ) -> None:
        self._strategy = strategy

    def chunk(
        self,
        document: Document,
    ) -> ChunkingResult:

        return self._strategy.split(
            document,
        )