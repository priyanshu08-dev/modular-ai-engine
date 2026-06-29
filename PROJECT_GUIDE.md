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

Current request flow:

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
Prompt Manager
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

This flow will evolve over time, but the API layer should remain stable.

---

# 3. Current Folder Structure

```text
backend/

app/
│
├── api/
├── config/
├── engine/
├── providers/
├── schemas/
├── services/
│
└── main.py
```

Every folder has one responsibility.

No folder should perform another folder's job.

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

* Execute AI requests
* Build AI execution flow
* Manage prompts
* Manage request state

Future responsibilities

* Execution Pipeline
* Conversation Memory
* Retrieval-Augmented Generation
* Planning
* Tool execution
* LangGraph orchestration
* Multi-agent workflows

The engine should become the single place where AI reasoning happens.

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

Central execution engine.

Current responsibilities

* Receive user message
* Obtain prompt
* Obtain provider
* Execute request
* Return response

Future responsibilities

* Conversation memory
* Retrieval
* Planning
* Tool execution
* LangGraph

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

## EngineState

Purpose

Represent one AI execution.

Current

Stores

* User message

Future

Will also contain

* Conversation ID
* Memory
* Retrieved documents
* Metadata
* Token usage
* Latency
* Provider information

---

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
AIEngine

uses

↓

PromptManager
```

```text
AIEngine

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

PromptManager

↓

ProviderFactory

↓

GroqProvider

↓

ChatGroq

↓

Groq API

↓

Response
```

At this stage the engine acts as a centralized execution layer.

Future milestones will extend this flow rather than replacing it.

---

# 10. Planned Evolution

The engine is intentionally designed to grow.

Current

```text
AIEngine

↓

Provider
```

Planned

```text
AIEngine

↓

Execution Pipeline

↓

Conversation Memory

↓

Retrieval

↓

Prompt Construction

↓

Tool Calling

↓

LangGraph

↓

Provider
```

Every new capability should plug into this pipeline without requiring changes to the API layer.

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
