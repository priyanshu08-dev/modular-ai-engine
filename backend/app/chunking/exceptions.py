class ChunkingError(Exception):
    """
    Base exception for the chunking subsystem.
    """


class InvalidChunkError(ChunkingError):
    """
    Raised when an invalid chunk is created.
    """


class ChunkingStrategyError(ChunkingError):
    """
    Raised when a chunking strategy fails.
    """


class ChunkConfigurationError(ChunkingError):
    """
    Raised for invalid chunk configuration.
    """