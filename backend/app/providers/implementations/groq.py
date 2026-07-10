from collections.abc import AsyncIterator

from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq

from app.config.settings import settings
from app.providers.base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY,
            temperature=0.3,
        )

    def get_chat_model(self) -> ChatGroq:
        return self.llm

    async def stream(
        self,
        messages: list[BaseMessage],
    ) -> AsyncIterator[str]:

        async for chunk in self.llm.astream(messages):

            if chunk.content:
                yield chunk.content