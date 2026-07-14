from fastapi import UploadFile

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
