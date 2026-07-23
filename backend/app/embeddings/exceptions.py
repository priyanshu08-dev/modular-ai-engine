class EmbeddingError(Exception):
    """
    Base exception for all embedding-related errors.
    """


class EmbeddingProviderError(EmbeddingError):
    """
    Raised when an embedding provider fails to generate embeddings.
    """


class UnsupportedEmbeddingProviderError(EmbeddingError):
    """
    Raised when the configured embedding provider is unsupported.
    """


class InvalidEmbeddingInputError(EmbeddingError):
    """
    Raised when invalid input is supplied for embedding generation.
    """