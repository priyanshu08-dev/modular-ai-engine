class DocumentError(Exception):
    """
    Base exception for all document-related errors.
    """


class UnsupportedDocumentError(DocumentError):
    """
    Raised when the document format is not supported.
    """


class InvalidDocumentError(DocumentError):
    """
    Raised when the uploaded document is invalid,
    empty, missing or exceeds configured limits.
    """


class DocumentParsingError(DocumentError):
    """
    Raised when a parser fails to extract text
    from an otherwise valid document.
    """