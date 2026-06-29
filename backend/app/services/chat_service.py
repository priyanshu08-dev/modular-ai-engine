from app.providers import ProviderFactory


class ChatService:

    def __init__(self):

        provider = ProviderFactory.get_provider()

        self.llm = provider.get_chat_model()

    async def chat(self, message: str):

        response = await self.llm.ainvoke(message)

        return response.content