from abc import ABC, abstractmethod

from langchain_core.language_models.chat_models import BaseChatModel


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