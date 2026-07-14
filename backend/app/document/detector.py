from pathlib import Path

import magic

from app.config.settings import settings
from app.document.exceptions import (
    InvalidDocumentError,
    UnsupportedDocumentError,
)
from app.document.models import DocumentType


class DocumentDetector:
    """
    Detects and validates uploaded documents.

    Responsibilities:
    - Verify file exists.
    - Verify file is not empty.
    - Verify file size.
    - Detect MIME type using python-magic.
    - Resolve DocumentType.
    """

    SUPPORTED_DOCUMENTS = {
        "application/pdf": DocumentType.PDF,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocumentType.DOCX,
        "text/plain": DocumentType.TXT,
    }

    @classmethod
    def detect(
        cls,
        file_path: Path,
    ) -> DocumentType:
        

        file_size = file_path.stat().st_size

        # -------------------------
        # File existence
        # -------------------------

        if not file_path.exists():
            raise InvalidDocumentError(
                f"Document '{file_path}' does not exist."
            )

        # -------------------------
        # Empty file
        # -------------------------

        if file_size == 0:
            raise InvalidDocumentError(
                f"Document '{file_path.name}' is empty."
            )

        # -------------------------
        # File size
        # -------------------------

        max_size = settings.MAX_DOCUMENT_SIZE_MB * 1024 * 1024

        if file_size > max_size:
            raise InvalidDocumentError(
                f"Document '{file_path.name}' exceeds the maximum allowed size "
                f"of {settings.MAX_DOCUMENT_SIZE_MB} MB."
            )

        # -------------------------
        # MIME detection
        # -------------------------

        mime_type = magic.from_file(
            str(file_path),
            mime=True,
        )

        # -------------------------
        # Markdown handling
        # -------------------------

        if (
            mime_type == "text/plain"
            and file_path.suffix.lower() == ".md"
        ):
            return DocumentType.MARKDOWN

        # -------------------------
        # Supported document
        # -------------------------

        document_type = cls.SUPPORTED_DOCUMENTS.get(
            mime_type,
        )

        if document_type is None:
            raise UnsupportedDocumentError(
                f"Unsupported document type.\n"
                f"Detected MIME type: '{mime_type}'."
            )

        return document_type