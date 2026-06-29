from langchain_core.messages import HumanMessage, SystemMessage

from app.engine.prompt_manager import PromptManager
from app.engine.router import EngineRouter
from app.engine.state import EngineState
from app.providers import ProviderFactory


class AIEngine:

    def __init__(self):

        provider = ProviderFactory.get_provider()

        self.llm = provider.get_chat_model()

        self.router = EngineRouter()

    async def run(
        self,
        message: str,
    ) -> str:

        state = EngineState(
            user_message=message,
        )

        if self.router.should_use_rag(state):

            raise NotImplementedError(
                "RAG not implemented."
            )

        response = await self.llm.ainvoke(
            [
                SystemMessage(
                    PromptManager.get_default_prompt(),
                ),
                HumanMessage(
                    message,
                ),
            ]
        )

        return response.content