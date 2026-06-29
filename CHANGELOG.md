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
