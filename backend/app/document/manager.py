from pathlib import Path

from app.document.detector import DocumentDetector
from app.document.models import Document
from app.document.parser_factory import DocumentParserFactory


class DocumentManager:
    """
    Coordinates document parsing.

    The manager knows nothing about parser implementations.
    """

    @classmethod
    def parse(
        cls,
        file_path: Path,
    ) -> Document:
        document_type = DocumentDetector.detect(
            file_path,
        )

        parser = DocumentParserFactory.get_parser(
            document_type,
        )

        return parser.parse(
            file_path,
        )
