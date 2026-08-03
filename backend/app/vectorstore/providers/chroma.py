from __future__ import annotations

import asyncio

import chromadb
from app.config.settings import settings
from app.vectorstore.exceptions import (
    CollectionNotFoundError,
    VectorSearchError,
    VectorStorageError,
)
from app.vectorstore.models import VectorBatch
from app.vectorstore.providers.base import BaseVectorStoreProvider
from chromadb.api.models.Collection import Collection


class ChromaVectorStoreProvider(BaseVectorStoreProvider):
    """
    ChromaDB implementation of the Vector Store provider.
    """

    def __init__(self) -> None:
        self._client = chromadb.PersistentClient(
            path=settings.CHROMADB_PATH,
        )
        self._collections: dict[str, Collection] = {}

    def _get_collection(
        self,
        collection_name: str,
    ) -> Collection:
        """
        Returns a cached collection instance.
        """
        collection = self._collections.get(collection_name)

        if collection is None:
            collection = self._client.get_or_create_collection(
                name=collection_name,
            )
            self._collections[collection_name] = collection

        return collection

    async def store(
        self,
        collection_name: str,
        batch: VectorBatch,
    ) -> None:
        collection = self._get_collection(
            collection_name
        )

        try:
            await asyncio.to_thread(
                collection.add,
                ids=[vector.embedding_id for vector in batch.vectors],
                documents=[vector.content for vector in batch.vectors],
                embeddings=[vector.vector for vector in batch.vectors],
                metadatas=[vector.metadata for vector in batch.vectors],
            )
        except Exception as exc:
            raise VectorStorageError(
                "Failed to store vectors in ChromaDB."
            ) from exc

    async def similarity_search(
        self,
        collection_name: str,
        query_embedding: list[float],
        limit: int = 5,
        where: dict[str, object] | None = None,
    ) -> list[dict]:
        collection = self._get_collection(collection_name)

        try:
            return await asyncio.to_thread(
                collection.query,
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where,
            )
        except Exception as exc:
            raise VectorSearchError(
                "Failed to perform similarity search."
            ) from exc

    async def delete_document(
        self,
        collection_name: str,
        document_id: str,
    ) -> None:
        collection = self._get_collection(collection_name)

        try:
            await asyncio.to_thread(
                collection.delete,
                where={
                    "document_id": document_id,
                },
            )
        except Exception as exc:
            raise VectorStorageError(
                "Failed to delete document vectors."
            ) from exc

    async def delete_collection(
        self,
        collection_name: str,
    ) -> None:
        try:
            await asyncio.to_thread(
                self._client.delete_collection,
                collection_name,
            )

            self._collections.pop(
                collection_name,
                None,
            )
        except Exception as exc:
            raise VectorStorageError(
                "Failed to delete collection."
            ) from exc

    async def collection_exists(
        self,
        collection_name: str,
    ) -> bool:
        try:
            collections = await asyncio.to_thread(
                self._client.list_collections,
            )

            return any(
                collection.name == collection_name
                for collection in collections
            )
        except Exception:  # noqa: BLE001
            return False

    async def count(
        self,
        collection_name: str,
    ) -> int:
        collection = self._get_collection(collection_name)

        try:
            return await asyncio.to_thread(
                collection.count,
            )
        except Exception as exc:
            raise CollectionNotFoundError(
                "Failed to retrieve vector count."
            ) from exc