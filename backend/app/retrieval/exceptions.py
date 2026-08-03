class RetrievalError(Exception):
    """
    Base exception for all retrieval-related errors.
    """


class EmptyQueryError(RetrievalError):
    """
    Raised when an empty query string is supplied for retrieval.
    """


class InvalidScoreThresholdError(RetrievalError):
    """
    Raised when an invalid similarity score threshold is configured.
    """


class SearchExecutionError(RetrievalError):
    """
    Raised when the underlying retrieval strategy fails.
    """
