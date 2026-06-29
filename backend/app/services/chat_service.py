from app.engine import AIEngine


class ChatService:

    def __init__(self):

        self.engine = AIEngine()

    async def chat(
        self,
        message: str,
    ) -> str:

        return await self.engine.run(message)