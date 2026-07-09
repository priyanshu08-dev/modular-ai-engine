from abc import ABC, abstractmethod

from langchain_core.messages import BaseMessage


class BaseMemoryStore(ABC):
    """
    Base interface for all conversation memory stores.
    """

    @abstractmethod
    async def get_messages(
        self,
        conversation_id: str,
    ) -> list[BaseMessage]:
        """
        Retrieve all messages for a conversation.
        """
        pass

    @abstractmethod
    async def save_messages(
        self,
        conversation_id: str,
        messages: list[BaseMessage],
    ) -> None:
        """
        Persist one or more messages.
        """
        pass

    @abstractmethod
    async def clear(
        self,
        conversation_id: str,
    ) -> None:
        """
        Delete a conversation.
        """
        pass