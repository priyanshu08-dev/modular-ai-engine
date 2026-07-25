from fastapi import UploadFile

from app.chunking.manager import ChunkManager
from app.chunking.models import ChunkingResult
from app.chunking.strategies.recursive import RecursiveChunkingStrategy
from app.document.manager import DocumentManager
from app.document.models import Document
from app.document.storage import DocumentStorage
from app.vectorstore.manager import VectorStoreManager


class DocumentService:
    """
    Handles document-related use cases.
    """

    def __init__(self) -> None:
        self._vectorstore_manager = VectorStoreManager()

    async def parse_document(
        self,
        file: UploadFile,
    ) -> Document:

        file_path = DocumentStorage.save(
            file,
        )

        return DocumentManager.parse(
            file_path,
        )

    async def parse_and_chunk(
        self,
        file: UploadFile,
    ) -> ChunkingResult:

        document = await self.parse_document(
            file,
        )

        manager = ChunkManager(
            RecursiveChunkingStrategy(),
        )

        return manager.chunk(
            document,
        )

    async def ingest_document(
        self,
        file_path: str,
    ):
        """
        Parses a document, chunks it, generates embeddings,
        and stores them inside the configured vector store.
        """

        chunking_result = await self.parse_and_chunk(
            file_path,
        )

        embedding_result = (
            await self._embedding_manager.generate_embeddings(
                chunking_result,
            )
        )

        await self._vectorstore_manager.store_embeddings(
            chunking_result,
            embedding_result,
        )

        return embedding_result