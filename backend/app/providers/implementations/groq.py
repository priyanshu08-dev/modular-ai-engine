from langchain_groq import ChatGroq

from app.config.settings import settings
from app.providers.base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    def get_chat_model(self):

        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY,
            temperature=0.3,
        )