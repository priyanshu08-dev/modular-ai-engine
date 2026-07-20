from app.chunking.strategies.base import BaseChunkingStrategy


class SemanticChunkingStrategy(BaseChunkingStrategy):
    """
    Placeholder for semantic chunking.

    Will be implemented in a future milestone.
    """

    def split(self, document):
        raise NotImplementedError(
            "Semantic chunking has not been implemented yet."
        )