import uuid

from langchain_core.messages import BaseMessage

from app.engine.memory.base import BaseMemoryStore


class MemoryManager:
    """
    Coordinates conversation memory independently of
    the underlying storage implementation.
    """

    def __init__(
        self,
        store: BaseMemoryStore,
    ):
        self.store = store

    def get_or_create_conversation_id(
        self,
        conversation_id: str | None,
    ) -> str:

        if conversation_id:
            return conversation_id

        return str(uuid.uuid4())

    async def get_messages(
        self,
        conversation_id: str,
    ) -> list[BaseMessage]:

        return await self.store.get_messages(
            conversation_id,
        )

    async def save_messages(
        self,
        conversation_id: str,
        messages: list[BaseMessage],
    ) -> None:

        await self.store.save_messages(
            conversation_id,
            messages,
        )

    async def clear(
        self,
        conversation_id: str,
    ) -> None:

        await self.store.clear(
            conversation_id,
        )