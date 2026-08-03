from abc import ABC, abstractmethod

from app.retrieval.models import RetrievalRequest, RetrievalResult


class BaseRetrievalStrategy(ABC):
    """
    Abstract interface for all retrieval strategies.
    """

    @abstractmethod
    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:
        """
        Executes semantic search for a given retrieval request.
        """
        pass
