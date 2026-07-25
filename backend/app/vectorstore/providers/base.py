from __future__ import annotations

from abc import ABC, abstractmethod

from app.vectorstore.models import VectorBatch


class BaseVectorStoreProvider(ABC):
    """
    Base interface implemented by every
    vector database provider.
    """

    @abstractmethod
    async def store(
        self,
        collection_name: str,
        batch: VectorBatch,
    ) -> None:
        """
        Persist every vector contained inside
        the supplied VectorBatch.
        """


    @abstractmethod
    async def similarity_search(
        self,
        collection_name: str,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:
        """
        Perform similarity search.
        """


    @abstractmethod
    async def delete_document(
        self,
        collection_name: str,
        document_id: str,
    ) -> None:
        """
        Delete every vector belonging to
        the supplied document.
        """


    @abstractmethod
    async def delete_collection(
        self,
        collection_name: str,
    ) -> None:
        """
        Delete an entire collection.
        """


    @abstractmethod
    async def collection_exists(
        self,
        collection_name: str,
    ) -> bool:
        """
        Returns True if the supplied
        collection exists.
        """


    @abstractmethod
    async def count(
        self,
        collection_name: str,
    ) -> int:
        """
        Returns the number of vectors
        stored inside the collection.
        """
