from app.config.settings import settings

from app.providers.implementations.groq import GroqProvider
from app.providers.implementations.openai import OpenAIProvider
from app.providers.implementations.gemini import GeminiProvider


class ProviderFactory:

    @staticmethod
    def get_provider():

        provider = settings.LLM_PROVIDER.lower()

        if provider == "groq":
            return GroqProvider()

        if provider == "openai":
            return OpenAIProvider()

        if provider == "gemini":
            return GeminiProvider()

        raise ValueError(
            f"Unsupported provider: {provider}"
        )