from app.config.settings import settings
from app.vectorstore.exceptions import (
    UnsupportedVectorStoreProviderError,
)
from app.vectorstore.providers.base import (
    BaseVectorStoreProvider,
)
from app.vectorstore.providers.chroma import (
    ChromaVectorStoreProvider,
)


class VectorStoreFactory:

    _provider: BaseVectorStoreProvider | None = None

    @classmethod
    def get_provider(cls) -> BaseVectorStoreProvider:

        if cls._provider is None:
            provider = settings.VECTORSTORE_PROVIDER.lower()

            if provider == "chromadb":
                cls._provider = ChromaVectorStoreProvider()
            else:
                raise UnsupportedVectorStoreProviderError(...)

        return cls._provider