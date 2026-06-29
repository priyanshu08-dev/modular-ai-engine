from dataclasses import dataclass


@dataclass(slots=True)
class EngineState:

    user_message: str