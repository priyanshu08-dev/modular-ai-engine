from app.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):

    def get_chat_model(self):
        raise NotImplementedError(
            "OpenAI provider not implemented yet."
        )