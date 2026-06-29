class PromptManager:
    """
    Central place to manage system prompts.
    """

    DEFAULT_SYSTEM_PROMPT = """
You are Modular AI Engine.

You are an intelligent reasoning assistant.

Provide accurate, concise and structured answers.
""".strip()

    @classmethod
    def get_default_prompt(cls) -> str:
        return cls.DEFAULT_SYSTEM_PROMPT