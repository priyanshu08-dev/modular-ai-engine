from app.rag.models import RAGContext


class RAGPromptBuilder:
    """
    Constructs grounded system prompts incorporating retrieved knowledge context.
    """

    DEFAULT_GROUNDED_INSTRUCTIONS = """
You are Modular AI Engine, a production-grade reasoning assistant equipped with retrieved knowledge.

CRITICAL GROUNDING INSTRUCTIONS:
1. Answer the user's question accurately using ONLY the provided Source Context below.
2. If the context contains sufficient information, provide a structured, detailed answer and cite your sources using bracketed citations such as [Source 1], [Source 2], etc.
3. If the provided context does NOT contain enough information to answer the question, state clearly and concisely: "The provided knowledge base does not contain sufficient information to answer this question."
4. Do NOT attempt to fabricate, hallucinate, or extrapolate facts beyond the explicit content provided in the sources.

=== RETRIEVED SOURCE CONTEXT ===
{context_text}
================================
""".strip()

    NO_CONTEXT_FALLBACK_PROMPT = """
You are Modular AI Engine, an intelligent reasoning assistant.

NOTICE: Knowledge base search was performed for the user's request, but no relevant document chunks passed the similarity score threshold.

State clearly to the user that no relevant information was found in the uploaded documents for their query, and then answer their question using your general reasoning capabilities, explicitly noting that the response is NOT derived from uploaded documents.
""".strip()

    @classmethod
    def build_system_prompt(
        cls,
        rag_context: RAGContext,
    ) -> str:
        """
        Builds system prompt based on context availability.
        """
        if rag_context.has_relevant_context:
            return cls.DEFAULT_GROUNDED_INSTRUCTIONS.format(
                context_text=rag_context.formatted_context,
            )
        return cls.NO_CONTEXT_FALLBACK_PROMPT
