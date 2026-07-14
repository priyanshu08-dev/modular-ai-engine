from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from app.document.exceptions import DocumentParsingError
from app.document.models import Document, DocumentMetadata, DocumentType


class BaseDocumentParser(ABC):
    """
    Base class for all document parsers.

    Implements the complete parsing workflow using the
    Template Method pattern.
    """

    DOCUMENT_TYPE: DocumentType
    MIME_TYPE: str

    def parse(
        self,
        file_path: Path,
    ) -> Document:
        try:
            document = self.load(file_path)

            content = self.extract_text(document)

            metadata = DocumentMetadata(
                filename=file_path.name,
                extension=file_path.suffix.lower(),
                mime_type=self.MIME_TYPE,
                size=file_path.stat().st_size,
                page_count=self.get_page_count(document),
                character_count=len(content),
                word_count=len(content.split()),
            )

            return Document(
                document_type=self.DOCUMENT_TYPE,
                content=content,
                metadata=metadata,
            )

        except Exception as exc:
            raise DocumentParsingError(
                f"Failed to parse '{file_path.name}' "
                f"using {self.__class__.__name__}."
            ) from exc

    @abstractmethod
    def load(
        self,
        file_path: Path,
    ) -> Any:
        """
        Load the document into memory.
        """

    @abstractmethod
    def extract_text(
        self,
        document: Any,
    ) -> str:
        """
        Extract text from the loaded document.
        """

    def get_page_count(
        self,
        document: Any,
    ) -> int | None:
        """
        Override only for formats supporting pages.
        """
        return None
