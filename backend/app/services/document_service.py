from fastapi import UploadFile

from app.chunking.manager import ChunkManager
from app.chunking.models import ChunkingResult
from app.chunking.strategies.recursive import RecursiveChunkingStrategy
from app.document.manager import DocumentManager
from app.document.models import Document
from app.document.storage import DocumentStorage


class DocumentService:
    """
    Handles document-related use cases.
    """

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