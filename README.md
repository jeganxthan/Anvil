# Anvil

> **The Open-Source AI Workspace**
>
> One desktop application for every AI model, every workflow, and every developer.

---

## Vision

Anvil aims to become the **VS Code of AI**.

Instead of forcing users to switch between ChatGPT, Claude, Gemini, Ollama, LM Studio, Open WebUI, NotebookLM, and dozens of AI tools, Anvil provides a single, extensible desktop platform where every model, every workflow, and every AI technique works together.

Our goal is to build an AI workspace that developers, researchers, students, and enterprises can customize and extend.

---

# Why Anvil?

Modern AI applications are fragmented.

* ChatGPT for writing
* Claude for long context
* Gemini for multimodal tasks
* Ollama for local models
* Open WebUI for self-hosting
* LM Studio for local inference
* NotebookLM for research
* Pinecone for vectors
* LangChain for orchestration
* CrewAI for agents

Anvil brings everything together.

---

# Core Principles

* Open Source
* Privacy First
* Local First
* Multi-Provider
* Extensible
* Fast
* Cross Platform
* Developer Friendly
* Plugin Based

---

# Architecture

```text
                React + TypeScript

                        │

                Tauri Desktop (Rust)

                        │

        ┌───────────────┴────────────────┐
        │                                │

   Rust Core Engine                Python AI Engine

        │                                │

 Filesystem                   LangChain
 Database                     LlamaIndex
 Plugins                      LangGraph
 IPC                          CrewAI
 Settings                     AutoGen
 Cache                        DSPy
 Authentication               RAG
 Streaming                    Embeddings
 Encryption                   OCR
                               Vision
                               Speech
                               Evaluation

                        │

                 AI Provider Layer

                        │

 OpenAI
 Anthropic
 Google Gemini
 NVIDIA NIM
 Ollama
 Groq
 OpenRouter
 TogetherAI
 DeepSeek
 Mistral
 Azure OpenAI
 AWS Bedrock

                        │

          Vector Databases / Storage

 Pinecone
 Qdrant
 FAISS
 Chroma
 LanceDB
 SQLite
 PostgreSQL
 Redis
```

---

# Features

## AI Providers

* NVIDIA NIM
* OpenAI
* Gemini
* Claude
* Ollama
* Groq
* OpenRouter
* TogetherAI
* DeepSeek
* Mistral
* Azure OpenAI
* AWS Bedrock

---

## Local Models

* Ollama
* llama.cpp
* LM Studio
* vLLM
* SGLang

---

## RAG

* PDF Chat
* Word Documents
* Excel
* CSV
* Markdown
* HTML
* Websites
* GitHub Repositories
* YouTube Transcripts
* Notion
* Confluence
* Obsidian Vaults

---

## Embeddings

* BGE
* Nomic
* E5
* Jina
* OpenAI
* Voyage
* NVIDIA

---

## Vector Databases

* Pinecone
* Qdrant
* Chroma
* FAISS
* LanceDB
* Milvus
* Weaviate

---

## AI Techniques

* Retrieval-Augmented Generation (RAG)
* Hybrid Search
* Semantic Search
* Metadata Filtering
* Multi Query Retrieval
* Context Compression
* Re-ranking
* Long-Term Memory
* Conversation Memory
* Prompt Templates
* Function Calling
* Tool Calling
* Structured Output
* Streaming Responses

---

## AI Frameworks

* LangChain
* LlamaIndex
* LangGraph
* CrewAI
* AutoGen
* Haystack
* DSPy

---

## Agents

* Research Agent
* Coding Agent
* Documentation Agent
* File Agent
* Browser Agent
* Database Agent
* GitHub Agent
* Terminal Agent
* Planner Agent
* Multi-Agent Workflows

---

## Workspace

* Projects
* Chat History
* Prompt Library
* Model Profiles
* Workspaces
* Collections
* Tags
* Search
* Export

---

## Developer Tools

* REST API
* Plugin SDK
* Rust SDK
* Python SDK
* Extension Marketplace
* CLI
* MCP Support (planned)

---

# Technology Stack

## Frontend

* React
* TypeScript
* Tailwind CSS
* Tauri

## Core

* Rust

## AI

* Python

## AI Frameworks

* LangChain
* LlamaIndex
* LangGraph
* CrewAI
* AutoGen
* DSPy

## Databases

* SQLite
* PostgreSQL
* Redis

## Vector Databases

* Pinecone
* Qdrant
* FAISS
* Chroma
* LanceDB

---

# Project Structure

```text
anvil/

apps/
    desktop/
    cli/

frontend/

src-tauri/
    commands/
    providers/
    config/
    settings/
    plugins/
    cache/
    database/
    ipc/
    updater/

python/
    api/
    providers/
    rag/
    embeddings/
    agents/
    workflows/
    loaders/
    memory/
    evaluation/
    tools/

docs/

plugins/

examples/

tests/

website/
```

---

# Roadmap

## v0.1

* NVIDIA Provider
* OpenAI Compatible Client
* Basic Chat
* Streaming
* Chat History
* Settings

---

## v0.2

* OpenAI
* Gemini
* Claude
* Ollama

---

## v0.3

* RAG
* Embeddings
* PDF Chat
* Pinecone
* FAISS

---

## v0.4

* LangChain
* LlamaIndex
* Memory
* Prompt Templates

---

## v0.5

* Agents
* CrewAI
* LangGraph
* AutoGen

---

## v1.0

* Plugin Marketplace
* Multi-Agent Workspace
* Enterprise Authentication
* Cloud Sync
* Team Collaboration
* Workflow Builder

---

# Contributing

We welcome developers of all experience levels.

Areas where you can contribute:

* Rust
* Python
* React
* AI
* Documentation
* Testing
* UI/UX
* Plugin Development
* Examples
* Tutorials

Please read `CONTRIBUTING.md` before submitting a pull request.

---

# License

MIT License

---

# Long-Term Goal

Anvil is not intended to be another chatbot.

It is intended to become an extensible AI operating environment where developers can build, run, compare, evaluate, and automate AI workflows using any model, any provider, and any retrieval system from one unified desktop application.
