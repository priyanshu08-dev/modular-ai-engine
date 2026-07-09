# Project Guide

> Complete developer guide for the Modular AI Engine.

This document explains how the project is organized, how every folder and file works, how requests travel through the application, and how every component connects with the others.

Unlike the README, this guide is intended for developers who want to understand or contribute to the codebase.

---

# 1. Project Purpose

The Modular AI Engine is **not** a chatbot.

It is a reusable AI backend that can eventually power multiple kinds of applications.

Examples include:

* Healthcare assistants
* Educational platforms
* Research copilots
* Enterprise AI
* Legal assistants
* Business intelligence
* Personal AI assistants

The backend is designed so that applications only communicate with one API, while the AI Engine handles all reasoning internally.

---

# 2. High-Level Request Flow

CCurrent request flow:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
API Router
   │
   ▼
Chat Service
   │
   ▼
AI Engine
   │
   ▼
Execution Pipeline
   │
   ├── MemoryStep
   │
   └── ProviderStep
   │
   ▼
Provider Factory
   │
   ▼
Groq Provider
   │
   ▼
Groq API
   │
   ▼
AI Response
   │
   ▼
Chat Service
   │
   ▼
FastAPI
   │
   ▼
Client
```

The API layer remains stable while the execution pipeline can evolve internally as new AI capabilities are introduced.
---

# 3. Current Folder Structure

```text
backend/

app/
│
├── api/
├── config/
├── engine/
│   ├── pipeline/
│   │   └── steps/
│   ├── execution_context.py
│   ├── core.py
│   └── prompt_manager.py
├── providers/
├── schemas/
├── services/
│
└── main.py
```

The `engine` package now contains the execution pipeline responsible for orchestrating AI request processing.

---

# 4. Folder Responsibilities

---

## api/

Purpose

Receive and respond to HTTP requests.

Responsible for

* API endpoints
* Request validation
* Response serialization
* HTTP status codes

Never responsible for

* AI logic
* Provider communication
* Business rules

Example

```text
POST /chat

↓

ChatService
```

---

## config/

Purpose

Application configuration.

Responsible for

* Environment variables
* Settings
* Configuration management

Every part of the application imports configuration from here.

No configuration values should be hardcoded.

---

## services/

Purpose

Application use cases.

Responsible for coordinating business workflows.

Current example

```text
ChatService
```

The service layer coordinates requests.

It does **not** perform AI reasoning.

Instead it delegates that responsibility to the AI Engine.

---

## engine/

Purpose

The brain of the application.

Current responsibilities

- Coordinate AI execution.
- Manage the execution pipeline.
- Manage conversation memory.
- Manage execution context.
- Delegate requests to AI providers.

Future responsibilities

- Streaming
- Retrieval-Augmented Generation (RAG)
- Planning
- Tool Calling
- LangGraph orchestration
- Multi-agent workflows

The engine acts as the central orchestration layer for all AI capabilities.

---

## providers/

Purpose

Communicate with external AI providers.

Current providers

* Groq

Future providers

* OpenAI
* Gemini

Responsibilities

* Configure models
* Authenticate requests
* Return LangChain chat models

Never responsible for

* Business logic
* Prompt construction
* Routing

---

## schemas/

Purpose

Define API data contracts.

Responsible for

* Request models
* Response models
* Validation

The schemas describe **what enters and leaves the API**.

---

# 5. File Responsibilities

---

## main.py

Entry point of the FastAPI application.

Responsibilities

* Create the FastAPI application
* Register routers
* Configure startup/shutdown lifecycle

---

## settings.py

Loads every configuration value from the environment.

Examples

* App name
* Debug mode
* Provider selection
* API keys

All configuration should originate here.

---

## ChatService

Purpose

Coordinate chat-related application logic.

Current flow

```text
API

↓

ChatService

↓

AIEngine
```

The service should remain lightweight.

It should not communicate directly with providers.

---

## AIEngine

Purpose

Central orchestration engine.

Current responsibilities

* Create an ExecutionContext.
* Execute the ExecutionPipeline.
* Return the final AI response.

The AIEngine no longer performs prompt construction or provider communication directly.

Instead, it delegates execution to the pipeline, allowing new capabilities to be added without modifying the engine itself.

Future responsibilities

* Execute configurable workflows.
* Coordinate pipeline execution.
* Support LangGraph orchestration.

Every AI capability should plug into the engine instead of bypassing it.

---

## PromptManager

Purpose

Manage system prompts.

Current

One default prompt.

Future

* Chat prompts
* RAG prompts
* Summary prompts
* Research prompts
* Prompt versioning
* Dynamic loading

---

## ExecutionPipeline

Purpose

Coordinate AI execution through independent pipeline steps.

Current pipeline

```text
MemoryStep

↓

ProviderStep
```

Responsibilities

- Build LangChain message history.
- Retrieve conversation memory.
- Execute AI requests.
- Persist updated conversations.

Future pipeline steps

- StreamingStep
- RetrieverStep
- ToolStep
- RAGStep
- PlanningStep

The execution pipeline provides a modular architecture where new AI capabilities can be introduced without modifying the AI Engine.

---



## Pipeline Steps

Each pipeline step has one responsibility.

### PromptStep

Loads the system prompt into the ExecutionContext.

### ProviderStep

Obtains the configured LangChain model and performs the AI request.

Future steps will include conversation memory, retrieval, planning, tool execution, streaming, and persistence.


---


## ExecutionContext

Purpose

Represent the complete state of a single AI execution.

Current

Stores

- Conversation ID
- Input message
- LangChain message history
- Final response
- Execution metadata

Future

Will also contain

- Retrieved documents
- Tool results
- Streaming state
- Token usage
- Latency
- Provider information

ExecutionContext acts as the shared state object passed through every pipeline step.

---



## Memory Subsystem

Purpose

Provide a provider-independent conversation memory abstraction.

Components

- MemoryManager
- BaseMemoryStore
- InMemoryStore

Responsibilities

- Create conversation IDs.
- Retrieve conversation history.
- Persist conversation messages.
- Abstract memory storage implementation.

Future implementations

- RedisMemoryStore
- PostgreSQLMemoryStore
- VectorMemoryStore
- LangGraph State



## ProviderFactory

Purpose

Return the configured AI provider.

Configuration

```text
.env

↓

LLM_PROVIDER=groq
```

Current

```text
ProviderFactory

↓

GroqProvider
```

Future

```text
ProviderFactory

↓

Groq

OpenAI

Gemini
```

The rest of the application should never know which provider is active.

---

## GroqProvider

Purpose

Create and configure the LangChain Groq model.

Only this class knows how to communicate with Groq.

Future providers will follow the same interface.

---

# 6. Object Relationships

Current ownership:

```text
FastAPI

owns

↓

API Router
```

```text
API Router

owns

↓

ChatService
```

```text
ChatService

owns

↓

AIEngine
```

```text
```text
AIEngine

owns

↓

ExecutionPipeline
```

```text
ExecutionPipeline

executes

↓

PromptStep
```

```text
PromptStep

uses

↓

PromptManager
```

```text
ExecutionPipeline

executes

↓

ProviderStep
```

```text
ProviderStep

uses

↓

ProviderFactory
```

```text
ProviderFactory

creates

↓

GroqProvider
```
```

```text
ProviderFactory

creates

↓

GroqProvider
```

```text
GroqProvider

returns

↓

ChatGroq
```

This hierarchy keeps responsibilities clearly separated.

---

# 7. Import Relationships

Current dependency chain:

```text
main.py

↓

api/
```

```text
api/

↓

services/
```

```text
services/

↓

engine/
```

```text
engine/

↓

providers/
```

```text
providers/

↓

LangChain
```

```text
LangChain

↓

Groq API
```

Dependencies should always flow downward.

Lower layers must never import higher layers.

---

# 8. Engineering Rules

The project follows these rules.

### Rule 1

Every folder should answer one question.

---

### Rule 2

Business logic should never know implementation details.

---

### Rule 3

Configuration belongs only in `config/`.

---

### Rule 4

Providers are replaceable.

Changing

```text
LLM_PROVIDER=groq
```

to

```text
LLM_PROVIDER=openai
```

should never require changes to the service layer.

---

### Rule 5

The AI Engine is the only place where AI reasoning should occur.

---

### Rule 6

Files are created only when they have a clear responsibility or expected growth.

Avoid unnecessary abstractions.

---

# 9. Current State of the Engine

Current execution flow:

```text
User Message

↓

ChatService

↓

AIEngine

↓

ExecutionContext

↓

ExecutionPipeline

↓

MemoryStep

↓

ProviderStep

↓

ProviderFactory

↓

ChatGroq

↓

Groq API

↓

Response
```

Conversation history is automatically loaded and persisted through the memory subsystem, while the AI Engine remains responsible only for orchestration.

---

# 10. Planned Evolution

The execution pipeline is intentionally designed to grow.

Current

```text
ExecutionPipeline

↓

PromptStep

↓

ProviderStep
```

Planned

```text
ExecutionPipeline

↓

RoutingStep

↓

MemoryStep

↓

RetrieverStep

↓

RAGStep

↓

PromptStep

↓

ToolStep

↓

StreamingStep

↓

ProviderStep
```

New capabilities should be introduced as additional pipeline steps whenever possible, preserving the simplicity of the AIEngine.

---

# 11. Development Workflow

Every milestone follows the same workflow.

```text
Architecture

↓

Implementation

↓

Testing

↓

Git Commit

↓

Documentation Update
```

Only tested and working milestones are considered complete.

---

# 12. Guiding Principle

The Modular AI Engine is built as a reusable AI platform.

The objective is not to maximize the number of features.

The objective is to build a clean, modular and extensible architecture where new AI capabilities can be integrated with minimal changes to the existing codebase.
