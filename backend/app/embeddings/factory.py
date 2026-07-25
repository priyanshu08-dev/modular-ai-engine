from app.config.settings import settings
from app.embeddings.exceptions import (
    UnsupportedEmbeddingProviderError,
)
from app.embeddings.providers.base import BaseEmbeddingProvider
from app.embeddings.providers.gemini import GeminiEmbeddingProvider
from app.embeddings.providers.openai import OpenAIEmbeddingProvider


class EmbeddingFactory:
    @staticmethod
    def get_provider() -> BaseEmbeddingProvider:
        provider = settings.EMBEDDING_PROVIDER.lower()

        if provider == "gemini":
            return GeminiEmbeddingProvider()

        if provider == "openai":
            return OpenAIEmbeddingProvider()

        raise UnsupportedEmbeddingProviderError(
            f"Unsupported embedding provider: {provider}"
        )