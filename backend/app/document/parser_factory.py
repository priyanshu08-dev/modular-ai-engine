from app.document.exceptions import UnsupportedDocumentError
from app.document.models import DocumentType
from app.document.parsers.base import BaseDocumentParser
from app.document.parsers.docx_parser import DOCXParser
from app.document.parsers.markdown_parser import MarkdownParser
from app.document.parsers.pdf_parser import PDFParser
from app.document.parsers.txt_parser import TXTParser


class DocumentParserFactory:
    _PARSERS = {
        DocumentType.PDF: PDFParser,
        DocumentType.DOCX: DOCXParser,
        DocumentType.TXT: TXTParser,
        DocumentType.MARKDOWN: MarkdownParser,
    }

    @classmethod
    def get_parser(
        cls,
        document_type: DocumentType,
    ) -> BaseDocumentParser:
        parser = cls._PARSERS.get(document_type)

        if parser is None:
            raise UnsupportedDocumentError(
                f"Unsupported document type: {document_type}"
            )

        return parser()
