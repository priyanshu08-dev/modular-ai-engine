from fastapi import UploadFile

from app.chunking.manager import ChunkManager
from app.chunking.models import ChunkingResult
from app.chunking.strategies.recursive import RecursiveChunkingStrategy
from app.document.manager import DocumentManager
from app.document.models import Document
from app.document.storage import DocumentStorage
from app.embeddings.manager import EmbeddingManager
from app.vectorstore.manager import VectorStoreManager


class DocumentService:
    """
    Handles document parsing, chunking, and full vector database ingestion.
    """

    def __init__(self) -> None:
        self._embedding_manager = EmbeddingManager()
        self._vectorstore_manager = VectorStoreManager()

    async def parse_document(
        self,
        file: UploadFile,
    ) -> Document:
        """Saves file to storage and extracts text content."""
        file_path = DocumentStorage.save(file)
        return DocumentManager.parse(file_path)

    async def parse_and_chunk(
        self,
        file: UploadFile,
    ) -> tuple[Document, ChunkingResult]:
        """Parses an uploaded file and splits it into chunks."""
        document = await self.parse_document(file)
        chunk_manager = ChunkManager(RecursiveChunkingStrategy())
        chunking_result = chunk_manager.chunk(document)
        return document, chunking_result

    async def ingest_document(
        self,
        file: UploadFile,
    ) -> dict[str, object]:
        """
        Parses, chunks, generates embeddings, and persists vectors to ChromaDB.
        """
        document, chunking_result = await self.parse_and_chunk(file)

        embedding_result = await self._embedding_manager.generate_embeddings(
            chunking_result,
        )

        await self._vectorstore_manager.store_embeddings(
            chunking_result,
            embedding_result,
        )

        return {
            "document_id": document.document_id,
            "filename": document.metadata.filename,
            "document_type": document.document_type.value,
            "total_chunks": chunking_result.total_chunks,
            "status": "ingested",
        }
