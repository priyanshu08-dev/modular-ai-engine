from app.document.models import Document
from app.schemas.document import (
    DocumentMetadataResponse,
    DocumentResponse,
)


class DocumentMapper:
    """
    Maps internal Document models to API response DTOs.
    """

    @staticmethod
    def to_response(
        document: Document,
    ) -> DocumentResponse:

        return DocumentResponse(
            document_id=document.document_id,
            document_type=document.document_type.value,
            content=document.content,
            metadata=DocumentMetadataResponse(
                filename=document.metadata.filename,
                extension=document.metadata.extension,
                mime_type=document.metadata.mime_type,
                size=document.metadata.size,
                page_count=document.metadata.page_count,
                character_count=document.metadata.character_count,
                word_count=document.metadata.word_count,
            ),
        )