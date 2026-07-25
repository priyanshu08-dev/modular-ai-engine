from app.chunking.models import ChunkingResult
from app.config.settings import settings
from app.embeddings.models import EmbeddingResult
from app.vectorstore.factory import VectorStoreFactory
from app.vectorstore.mapper import VectorStoreMapper


class VectorStoreManager:
    """
    Coordinates vector storage operations.
    """

    def __init__(self) -> None:
        self._provider = VectorStoreFactory.get_provider()
        self._default_collection = (
            settings.DEFAULT_VECTOR_COLLECTION
        )

    async def store_embeddings(
        self,
        chunking_result: ChunkingResult,
        embedding_result: EmbeddingResult,
    ) -> None:

        batch = VectorStoreMapper.to_vector_batch(
            chunking_result,
            embedding_result,
        )

        await self._provider.store(
            collection_name=self._default_collection,
            batch=batch,
        )

    async def delete_document(
        self,
        document_id: str,
    ) -> None:

        await self._provider.delete_document(
            collection_name=self._default_collection,
            document_id=document_id,
        )

    async def delete_collection(
        self,
    ) -> None:

        await self._provider.delete_collection(
            self._default_collection,
        )

    async def collection_exists(
        self,
    ) -> bool:

        return await self._provider.collection_exists(
            self._default_collection,
        )

    async def count(
        self,
    ) -> int:

        return await self._provider.count(
            self._default_collection,
        )