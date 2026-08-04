class RAGError(Exception):
    """Base exception for all RAG-related errors."""


class ContextFormattingError(RAGError):
    """Raised when formatting retrieved chunks into prompt context fails."""


class RAGExecutionError(RAGError):
    """Raised when the RAG orchestration step encounters a runtime failure."""


class InvalidRAGConfigError(RAGError):
    """Raised when invalid parameters are supplied to the RAG subsystem."""
