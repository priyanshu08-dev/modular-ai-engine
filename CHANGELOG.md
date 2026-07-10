# Changelog

All notable changes to the Modular AI Engine project are documented in this file.

The project follows a milestone-based development process where each milestone represents a stable, tested checkpoint.

---

# Version 0.1.0

Initial development release.

---

## Milestone 1 — Project Initialization

### Added

* Initialized Git repository.
* Initialized backend project using `uv`.
* Configured Python 3.14 development environment.
* Adopted `pyproject.toml` for dependency management.
* Established initial backend project structure.
* Created virtual environment.
* Configured VS Code development environment.

### Architecture Decisions

* Selected FastAPI as the backend framework.
* Selected LangChain as the LLM abstraction framework.
* Planned LangGraph as the future orchestration engine.
* Planned ChromaDB as the vector database.
* Chose React + TypeScript for the future frontend.
* Adopted `uv` instead of `pip`.

---

## Milestone 2 — FastAPI Foundation

### Added

* FastAPI application.
* Application Factory pattern.
* Lifespan event handling.
* Environment configuration using Pydantic Settings.
* `.env` based configuration management.
* API router architecture.
* Health endpoint.
* Swagger API documentation.

### Changed

* Introduced layered backend architecture.
* Centralized application configuration.
* Established routing system for future endpoints.

---

## Milestone 3 — AI Chat Integration

### Added

* Chat API endpoint.
* Request and response schemas.
* Chat service layer.
* LangChain integration.
* Groq provider integration.
* First AI conversation workflow.

### Changed

* Introduced service layer between API and AI logic.
* Isolated LLM communication from HTTP layer.

---

## Milestone 4 — Provider Abstraction

### Added

* Base provider interface.
* Provider Factory.
* Groq provider implementation.
* OpenAI provider placeholder.
* Gemini provider placeholder.
* Environment-based provider selection.

### Changed

* Removed direct dependency on Groq from business logic.
* Introduced provider abstraction layer.
* Centralized provider creation through Provider Factory.

### Architecture Impact

The application can now switch AI providers without changing business logic.

---

## Milestone 5 — AI Engine

### Added

* AI Engine.
* Engine state management.
* Prompt Manager.
* Central AI execution layer.

### Changed

* Moved AI execution out of Chat Service.
* Introduced centralized prompt management.
* Established AI Engine as the future reasoning layer.

### Architecture Impact

All AI requests now flow through a single execution engine, creating a central point where future capabilities such as conversation memory, Retrieval-Augmented Generation (RAG), LangGraph orchestration, tool execution, and planning can be integrated without changing the API layer.

---

# Current Status

## Completed

* Project Initialization
* FastAPI Foundation
* AI Chat Integration
* Provider Abstraction
* AI Engine

---

## Next Planned Milestone

Execution Pipeline

The next milestone will transform the AI Engine from a simple request executor into a staged execution pipeline capable of supporting future routing, planning, memory, and Retrieval-Augmented Generation workflows.

---

## Future Milestones

* Conversation Memory
* Streaming Responses
* Document Upload
* Document Parsing
* Embeddings
* ChromaDB Integration
* Retrieval Pipeline
* Retrieval-Augmented Generation (RAG)
* LangGraph Integration
* Tool Calling
* Multi-Agent Workflows
* Production Deployment



## Milestone 6 — Project Documentation

### Added

- README.md for project overview, setup instructions, and usage.
- ARCHITECTURE.md documenting the system architecture, request flow, and component responsibilities.
- ROADMAP.md outlining completed milestones and future development plans.
- CHANGELOG.md for milestone-based project history.
- PROJECTGUIDE.md containing development philosophy, engineering principles, and project structure.

### Changed

- Established a standardized documentation structure for the project.
- Consolidated architectural documentation into dedicated documents to reduce duplication.
- Introduced milestone-based documentation updates as part of the development workflow.

### Notes

This milestone establishes a maintainable documentation foundation for the project. All future milestones will include synchronized updates to the README, Architecture, Roadmap, Changelog, and Project Guide to ensure the codebase and documentation evolve together.



## Milestone 7 — Execution Pipeline

### Added

- ExecutionPipeline for sequential request execution.
- ExecutionContext for sharing execution state across pipeline steps.
- PromptStep to populate system prompts.
- ProviderStep to execute requests using the configured LangChain provider.

### Changed

- Refactored AIEngine to delegate execution through the pipeline.
- Simplified orchestration responsibilities within the AI Engine.

### Removed

- Legacy engine routing placeholder (`router.py`).

### Notes

This milestone introduces the execution architecture that future components such as Memory, RAG, Tool Calling, Streaming, and LangGraph will build upon.


## Milestone 8 — Conversation Memory & LangChain Message Pipeline

### Added

- Conversation memory subsystem.
- MemoryManager to coordinate conversation lifecycle.
- BaseMemoryStore abstraction.
- InMemoryStore implementation for development.
- MemoryStep for conversation history management.
- Conversation ID support across the API.
- LangChain BaseMessage-based execution context.

### Changed

- Refactored ExecutionContext to use LangChain messages instead of individual prompt fields.
- Updated AIEngine to orchestrate memory-aware conversations.
- Refactored ProviderStep to consume LangChain message history directly.
- Introduced shared MemoryManager instance across the application.
- Updated chat API to support multi-turn conversations using conversation IDs.

### Removed

- PromptStep from the execution pipeline.
- Legacy prompt assembly using `system_prompt` and `user_message`.

### Architecture Impact

The AI Engine now supports stateful multi-turn conversations through a modular memory subsystem. Conversation history is represented using LangChain message objects, allowing future capabilities such as Retrieval-Augmented Generation (RAG), Tool Calling, Streaming, and LangGraph workflows to integrate naturally without further architectural changes.

## Milestone 9 — Streaming Responses

### Added

- Provider-independent streaming support.
- Streaming execution path in the AI Engine.
- Streaming pipeline execution.
- Streaming support in ProviderStep.
- Server-Sent Events (SSE) API responses.
- Base provider streaming interface.
- Groq streaming implementation.

### Changed

- AI Engine now supports both synchronous and streaming execution.
- ProviderStep refactored to use a single streaming implementation.
- Chat endpoint migrated from JSON responses to StreamingResponse.
- PipelineStep now provides a default streaming implementation.
- Streaming became the primary execution model while preserving synchronous execution through stream consumption.

### Architecture Impact

The AI Engine now supports real-time token streaming without compromising its layered architecture. Streaming remains provider-independent and is fully integrated into the existing execution pipeline. The SSE protocol establishes a stable foundation for future capabilities such as Retrieval-Augmented Generation (RAG), Tool Calling, LangGraph workflows, reasoning traces, and progress events.
