from collections import defaultdict

from langchain_core.messages import BaseMessage

from app.engine.memory.base import BaseMemoryStore


class InMemoryStore(BaseMemoryStore):
    """
    Temporary in-memory implementation.

    Intended only for development.
    """

    def __init__(self):
        self._store: dict[str, list[BaseMessage]] = defaultdict(list)

    async def get_messages(
        self,
        conversation_id: str,
    ) -> list[BaseMessage]:

        return list(self._store[conversation_id])

    async def save_messages(
        self,
        conversation_id: str,
        messages: list[BaseMessage],
    ) -> None:

        self._store[conversation_id].extend(messages)

    async def clear(
        self,
        conversation_id: str,
    ) -> None:

        self._store.pop(conversation_id, None)