from app.engine import AIEngine


class ChatService:

    def __init__(self):

        self.engine = AIEngine()

    async def chat(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> tuple[str, str]:

        return await self.engine.run(
            message=message,
            conversation_id=conversation_id,
        )