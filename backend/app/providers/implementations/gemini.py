from app.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):

    def get_chat_model(self):
        raise NotImplementedError(
            "Gemini provider not implemented yet."
        )