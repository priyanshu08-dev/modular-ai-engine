from dataclasses import dataclass, field
from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage


@dataclass
class ExecutionContext:
    """
    Carries state throughout a single AI execution.
    """

    # Unique conversation identifier.
    conversation_id: str 

    input_message: HumanMessage

    # Complete conversation represented as LangChain messages.
    messages: list[BaseMessage] = field(default_factory=list)

    # Final response returned by the pipeline.
    response: str | None = None

    # Additional execution data shared between pipeline steps.
    metadata: dict[str, Any] = field(default_factory=dict)