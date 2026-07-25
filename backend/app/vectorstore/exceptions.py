"""
Custom exceptions for the Vector Storage subsystem.
"""


class VectorStoreError(Exception):
    """
    Base exception for all vector storage related errors.
    """

class UnsupportedVectorStoreProviderError(VectorStoreError):
    """
    Raised when an unsupported vector store provider
    is configured.
    """


class CollectionAlreadyExistsError(VectorStoreError):
    """
    Raised when attempting to create an existing collection.
    """


class CollectionNotFoundError(VectorStoreError):
    """
    Raised when a collection cannot be located.
    """


class VectorStorageError(VectorStoreError):
    """
    Raised when embeddings cannot be stored.
    """


class VectorSearchError(VectorStoreError):
    """
    Raised when similarity search fails.
    """

class VectorDeletionError(VectorStoreError):
    """
    Raised when vectors cannot be deleted.
    """