from app.engine.state import EngineState


class EngineRouter:

    def should_use_rag(
        self,
        state: EngineState,
    ) -> bool:

        return False