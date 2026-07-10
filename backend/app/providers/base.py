from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage


class BaseLLMProvider(ABC):
    """
    Base class for all LLM providers.
    """

    @abstractmethod
    def get_chat_model(self) -> BaseChatModel:
        """
        Returns a configured LangChain chat model.
        """
        pass

    @abstractmethod
    async def stream(
        self,
        messages: list[BaseMessage],
    ) -> AsyncIterator[str]:
        """
        Streams the model response token-by-token.
        """
        pass