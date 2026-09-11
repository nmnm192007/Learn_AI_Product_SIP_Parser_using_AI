````markdown
# AI Based SIP Call Flow Analyser

An AI-powered SIP Call Flow Analyser that allows telecom engineers to upload SIP call-flow logs and ask natural-language questions about call events, failures, errors, call status, and session behaviour.

The product combines deterministic SIP log processing, semantic embeddings, vector search, controlled query expansion, and a local LLM to provide grounded answers from the uploaded call-flow data.

> **Project Status: V1 MVP – Working**
>
> V1 focuses on proving the complete AI product flow from SIP log ingestion to natural-language answering.
> Advanced retrieval optimisation, hybrid search, reranking, evaluation frameworks, cloud deployment and production hardening are planned for future versions.

---

## 1. Product Problem

Telecom and SIP engineers often need to investigate large call-flow logs to answer questions such as:

- Why did a SIP call fail?
- Which calls encountered errors?
- What caused the failure?
- Which call legs were terminated?
- What was the duration of a call?
- Did a particular SIP transaction complete successfully?
- What happened during a particular call flow?

Traditional troubleshooting requires engineers to manually search through large log files and correlate multiple SIP messages.

This product explores an AI-assisted approach where the engineer can upload the SIP trace and ask questions using natural language.

---

## 2. Product Vision

The long-term vision is to evolve this MVP into an AI-assisted telecom troubleshooting product capable of:

1. Understanding telecom/SIP logs
2. Reconstructing call/session context
3. Finding relevant evidence from large datasets
4. Explaining failures and call behaviour
5. Providing grounded answers with supporting evidence
6. Helping engineers reduce manual log-analysis effort

The current implementation represents the **V1 foundation** for this product.

---

# 3. V1 Capabilities

The current V1 implementation provides:

- SIP log file upload
- SIP log parsing
- Message normalization
- Call/session identification using Call-ID
- Session-based chunking
- Call status derivation
- Error extraction
- Semantic embedding generation
- Qdrant vector storage
- Semantic retrieval
- Deterministic query expansion
- Prompt construction
- Local LLM-based answer generation
- FastAPI REST API
- Swagger/OpenAPI interface
- Streamlit user interface

---

# 4. High-Level Architecture

```text
                         ┌─────────────────────┐
                         │      Streamlit      │
                         │     Web UI / MVP    │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │     REST API        │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                 Upload                            Query
                    │                               │
                    ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │ Log Ingestion   │             │ Query Expansion │
          └────────┬────────┘             └────────┬────────┘
                   │                               │
                   ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │ Parser          │             │ Query Embedding │
          └────────┬────────┘             └────────┬────────┘
                   │                               │
                   ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │ Normalizer      │             │ Qdrant Search   │
          └────────┬────────┘             └────────┬────────┘
                   │                               │
                   ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │ Sessionizer     │             │ Retrieved       │
          └────────┬────────┘             │ Context         │
                   │                      └────────┬────────┘
                   ▼                               │
          ┌─────────────────┐                       │
          │ Session Chunker │                       │
          └────────┬────────┘                       │
                   │                               │
                   ▼                               │
          ┌─────────────────┐                       │
          │ Chunk Enrichment│                       │
          └────────┬────────┘                       │
                   │                               │
                   ▼                               │
          ┌─────────────────┐                       │
          │ Sentence        │                       │
          │ Transformer     │                       │
          │ Embeddings      │                       │
          └────────┬────────┘                       │
                   │                               │
                   ▼                               │
          ┌─────────────────┐                       │
          │     Qdrant      │◄──────────────────────┘
          │  Vector Store   │
          └─────────────────┘

                         Query Answering
                              │
                              ▼
                    ┌─────────────────┐
                    │ Prompt Builder  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Ollama / Local  │
                    │      LLM        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ FastAPI Response│
                    │   + Streamlit   │
                    └─────────────────┘
````

---

# 5. End-to-End AI Pipeline

The product has two primary flows.

## 5.1 Document / Log Ingestion Flow

```text
SIP Log File
     │
     ▼
Parser
     │
     ▼
Normalizer
     │
     ▼
Sessionizer
     │
     ▼
Session Chunker
     │
     ▼
Chunk Enrichment
     │
     ▼
Embedding Preparation
     │
     ▼
Sentence Transformer
     │
     ▼
Vector Embeddings
     │
     ▼
Qdrant
```

### What happens?

The raw SIP trace is transformed into meaningful call/session-level information before it reaches the vector database.

Instead of embedding arbitrary lines from the log, V1 attempts to preserve useful telecom context such as:

* Call-ID
* Event type
* SIP messages
* Call status
* Error code
* Error text
* Session duration

This gives the embedding model a more meaningful representation of the underlying SIP event.

---

# 6. Query / Answer Flow

```text
User Question
      │
      ▼
Query Understanding
      │
      ▼
Deterministic Query Expansion
      │
      ▼
Query Embedding
      │
      ▼
Qdrant Semantic Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
Prompt Builder
      │
      ▼
Local LLM
      │
      ▼
Grounded Answer
```

For example:

```text
User:
"Show the internal server errors"

          ↓

Query Expansion:

"INTERNAL SERVER ERROR ERROR"

          ↓

Semantic Embedding

          ↓

Qdrant Search

          ↓

Relevant SIP chunks

          ↓

Prompt Builder

          ↓

LLM

          ↓

Answer:
"The internal server error is noted with error
code 500 and the call status is marked as failure."
```

The exact expansion depends on the deterministic domain vocabulary configured in the query expander.

---

# 7. Technology Stack

| Component        | Technology            | Purpose                            |
| ---------------- | --------------------- | ---------------------------------- |
| API              | FastAPI               | REST API layer                     |
| UI               | Streamlit             | Lightweight MVP UI                 |
| Language         | Python                | Application implementation         |
| Embeddings       | Sentence Transformers | Semantic representation            |
| Embedding Model  | `all-MiniLM-L6-v2`    | 384-dimensional embeddings         |
| Vector Database  | Qdrant                | Semantic vector retrieval          |
| LLM Runtime      | Ollama                | Local LLM inference                |
| LLM              | Local model           | Natural-language answer generation |
| Containerisation | Docker                | Application packaging              |
| Orchestration    | Kubernetes            | Planned deployment/hardening       |
| Cloud            | GCP                   | Planned cloud deployment           |
| IaC              | Terraform             | Planned infrastructure automation  |

---

# 8. Project Structure

```text
.
├── backend/
│   └── app/
│       ├── api/
│       │   ├── routes.py
│       │   └── upload.py
│       │
│       ├── ingestion/
│       │   ├── parser.py
│       │   ├── cleaner.py
│       │   ├── normalizer.py
│       │   ├── sessionizer.py
│       │   ├── chunk_sessions.py
│       │   ├── embedding_prep.py
│       │   └── pipeline.py
│       │
│       ├── retrieval/
│       │   ├── embedder.py
│       │   ├── retriever.py
│       │   ├── qdrant_client.py
│       │   ├── query_expander.py
│       │   └── emb_model_loader.py
│       │
│       ├── llm/
│       │   ├── llm_client.py
│       │   └── prompt_builder.py
│       │
│       ├── models/
│       │   └── ...
│       │
│       └── main.py
│
├── frontend/
│   ├── app.py
│   └── utils.py
│
├── data/
│   └── sip_flow_trace/
│
├── tests/
│   └── ...
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

> The exact structure may evolve as the product moves beyond V1.

---

# 9. API

## Root

```http
GET /
```

Returns basic service information.

---

## Health Check

```http
GET /health
```

Example:

```json
{
  "status": "healthy",
  "service": "AI SIP Logs Analyser",
  "version": "2.0"
}
```

---

## Upload SIP Log

```http
POST /files/upload
```

Uploads a SIP log file for processing.

The uploaded file is passed through the ingestion pipeline and converted into searchable vector representations.

---

## Query

```http
POST /query
```

Example request:

```json
{
  "query": "Why did the SIP call fail?"
}
```

The query is:

1. Understood
2. Expanded using deterministic domain rules
3. Converted into an embedding
4. Used to search Qdrant
5. Combined with retrieved context
6. Sent to the LLM
7. Returned as a natural-language answer

---

# 10. Running the Application

## Prerequisites

Install:

* Python 3.11+
* Git
* Ollama
* Qdrant
* Streamlit

Docker/Kubernetes are required only for the corresponding deployment setup.

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Activate on Linux/macOS:

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file based on:

```text
.env.example
```

Typical configuration includes the SIP log input location and LLM configuration.

---

# 11. Start Ollama

Make sure Ollama is running locally.

For example:

```bash
ollama serve
```

Pull the configured model if it is not already available:

```bash
ollama pull phi3
```

The exact model can be changed through the application configuration.

---

# 12. Start FastAPI

From the backend application directory:

```bash
uvicorn app.main:app --reload --reload-dir app
```

The API will be available through the configured local host/port.

Swagger/OpenAPI documentation:

```text
/docs
```

---

# 13. Start Streamlit

From the project root:

```bash
streamlit run frontend/app.py
```

The Streamlit UI can then be used to:

1. Upload a SIP log
2. Submit a natural-language question
3. View the generated answer

---

# 14. Example Questions

The MVP can be demonstrated using questions such as:

```text
Why did the SIP call fail?
```

```text
Show the internal server errors.
```

```text
What happened to the call leg?
```

```text
Show the failures and the reason behind them.
```

```text
Which calls were terminated successfully?
```

```text
What was the duration of the call?
```

---

# 15. AI / RAG Design

The product follows a Retrieval-Augmented Generation (RAG) pattern.

```text
             ┌──────────────────┐
             │     SIP Logs     │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Structured       │
             │ Processing       │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Enriched Chunks  │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Embedding Model  │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Qdrant           │
             └────────┬─────────┘
                      │
              Retrieval
                      │
                      ▼
             ┌──────────────────┐
             │ Relevant Context │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Prompt Builder   │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Local LLM        │
             └────────┬─────────┘
                      │
                      ▼
                  Answer
```

The LLM is not expected to independently understand the complete SIP trace.

Instead, relevant evidence is retrieved from the vector store and supplied to the LLM as context.

This reduces the dependency on the LLM's internal knowledge and allows answers to be based on the uploaded log data.

---

# 16. Why Session-Based Chunking?

A SIP call is not represented by a single log line.

A typical call may contain:

```text
INVITE
   ↓
100 TRYING
   ↓
180 RINGING
   ↓
200 OK
   ↓
ACK
   ↓
BYE
```

Errors may also occur within the same call/session.

Therefore, V1 groups messages around the call/session context instead of treating every log line as an independent document.

This improves the information available to the retrieval layer.

---

# 17. Why Enriched Embeddings?

Raw SIP messages can be difficult for a general embedding model to interpret consistently.

V1 therefore creates an enriched representation containing explicit semantic labels such as:

```text
Event Type
Call Status
Error
Error Code
Session Duration
SIP Messages
```

Example:

```text
SIP Call Flow Event ::

Event Type: ERROR

Messages: 500 INTERNAL SERVER ERROR

Call Status: FAILURE

Error: INTERNAL SERVER ERROR

Error Code: 500

Session Duration: 2.288 seconds
```

The enriched representation is used for embedding, while the original information remains available as structured metadata.

---

# 18. Why Deterministic Query Expansion?

V1 intentionally does not use an LLM to expand the user's query.

Instead, domain terminology is mapped using deterministic rules.

For example:

```text
"failed"
     ↓
"FAILURE"
```

```text
"call flow"
     ↓
"SIP CALL FLOW"
```

```text
"internal server error"
     ↓
"500 INTERNAL SERVER ERROR"
```

This provides:

* predictable behaviour
* explainability
* low latency
* no additional LLM dependency
* easy debugging
* easy extension with telecom vocabulary

The query expander is therefore a **controlled domain vocabulary layer**, rather than a general-purpose semantic paraphrasing engine.

---

# 19. Architectural Decisions

## FastAPI

Chosen as the API framework because it provides:

* REST API support
* request/response validation
* Pydantic integration
* automatic OpenAPI documentation
* asynchronous capabilities
* good fit for AI service architectures

---

## Streamlit

Chosen for V1 because the objective is to demonstrate the AI product workflow rather than spend significant development effort on frontend engineering.

A React-based frontend can be introduced later if required.

---

## Sentence Transformers

Used to generate semantic vector representations of SIP events.

V1 uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

with:

```text
384 dimensions
```

---

## Qdrant

Used as the vector database for semantic similarity search.

It provides a straightforward path from:

```text
Embedding
   ↓
Vector Storage
   ↓
Similarity Search
   ↓
Retrieved Context
```

---

## Ollama

Used to run the LLM locally.

This provides a low-cost development environment without requiring a paid external LLM API.

---

# 20. Current V1 Limitations

V1 is intentionally limited.

Known areas for improvement include:

* Retrieval quality varies depending on query formulation
* Query expansion currently uses deterministic rules
* Domain vocabulary is limited
* No hybrid keyword + vector retrieval
* No reranking layer
* No formal retrieval evaluation framework
* No comprehensive answer evaluation
* Limited evidence presentation in the UI
* Ingestion and query lifecycle can be further separated
* Vector persistence requires further production design
* Error handling can be hardened
* Authentication/authorization is not implemented
* Production observability is not yet implemented
* Cloud deployment is not yet the primary V1 focus

These are **known engineering opportunities**, not hidden defects.

The objective of V1 is to prove the complete AI product pipeline.

---

# 21. V2 Roadmap

The next iteration can focus on improving the system based on observations from V1.

### Retrieval

* Retrieval evaluation dataset
* Better query understanding
* YAML-based telecom vocabulary
* Multi-query retrieval
* Metadata filtering
* Hybrid search
* Reranking
* Improved chunking strategies

### AI Quality

* Answer evaluation
* Retrieval precision/recall analysis
* Grounding checks
* Better prompt strategies
* Evidence-aware answers

### Product

* Display supporting log evidence
* Show call/session details
* Better error explanations
* Improved UI
* Query history
* Multiple uploaded datasets

### Platform

* Better containerisation
* Kubernetes deployment
* Persistent Qdrant storage
* Health/readiness/liveness design
* Observability
* Configuration management

### Cloud

* GCP deployment
* Terraform infrastructure
* Cloud-native architecture
* CI/CD

---

# 22. V1 → V2 Engineering Mindset

An important design principle of this project is:

```text
Build
  ↓
Observe
  ↓
Measure
  ↓
Identify Weakness
  ↓
Make an Architectural Decision
  ↓
Implement Improvement
  ↓
Measure Again
```

For example:

```text
Query
  ↓
Low Retrieval Score
  ↓
Investigate Embedding Representation
  ↓
Enrich Chunk Representation
  ↓
Re-run Retrieval
  ↓
Observe Improvement
```

This iterative approach is intentionally part of the project.

---

# 23. What This Project Demonstrates

This project is not intended to demonstrate only "how to call an LLM."

It demonstrates the design and implementation of an AI-enabled product pipeline involving:

* Telecom domain understanding
* Log ingestion
* Data transformation
* Sessionisation
* Semantic chunking
* Embeddings
* Vector databases
* Retrieval
* Query understanding
* Prompt engineering
* Local LLM inference
* REST APIs
* UI integration
* Containerisation
* Kubernetes architecture
* AI system troubleshooting
* Iterative AI product improvement

---

# 24. Product Architecture Philosophy

The architecture follows a separation of responsibilities:

```text
UI
 ↓
API
 ↓
Business / AI Pipeline
 ↓
Retrieval
 ↓
Generation
```

Each stage should have a clear responsibility.

For example:

```text
Parser
    → Understand raw log structure

Normalizer
    → Make log data consistent

Sessionizer
    → Establish call/session context

Chunker
    → Create retrieval units

Embedding
    → Convert information into semantic vectors

Qdrant
    → Find relevant information

Query Expander
    → Improve retrieval-oriented representation

Prompt Builder
    → Construct LLM context

LLM
    → Generate natural-language explanation
```

This separation makes the system easier to debug, test and evolve.

---

# 25. Demo Flow

A simple product demonstration can follow this sequence:

### Step 1 – Upload

Upload a SIP trace file.

### Step 2 – Process

The backend parses and processes the call flows.

### Step 3 – Ask

Ask:

```text
Why did the SIP call fail?
```

### Step 4 – Retrieve

The system performs semantic search against the processed call/session chunks.

### Step 5 – Generate

Relevant context is supplied to the local LLM.

### Step 6 – Answer

The product returns a natural-language explanation.

### Step 7 – Explain the Architecture

The complete flow can then be explained as:

```text
User
 ↓
Streamlit
 ↓
FastAPI
 ↓
Ingestion
 ↓
Sessionisation
 ↓
Chunking
 ↓
Embedding
 ↓
Qdrant
 ↓
Retrieval
 ↓
Prompt
 ↓
LLM
 ↓
Answer
```

---

# 26. Future Direction

The long-term objective is to move from:

> **"Ask questions about SIP logs."**

towards:

> **"AI-assisted telecom troubleshooting and call-flow intelligence."**

Potential future capabilities include:

```text
SIP Log
   ↓
Call Reconstruction
   ↓
Failure Detection
   ↓
Root Cause Analysis
   ↓
Evidence
   ↓
Recommended Troubleshooting Actions
```

This can eventually evolve into a broader telecom AI product supporting:

* SIP troubleshooting
* protocol analysis
* product knowledge
* troubleshooting guides
* knowledge-base retrieval
* customer-care assistance
* engineering diagnostics

---

# 27. Disclaimer

This is an AI product development and architecture MVP intended for learning, experimentation, portfolio demonstration and architectural evaluation.

It should not be considered a production-grade telecom troubleshooting system.

---

# 28. Project Status

| Area                          | V1 Status |
| ----------------------------- | --------- |
| SIP log ingestion             | ✅         |
| Parsing                       | ✅         |
| Normalization                 | ✅         |
| Sessionisation                | ✅         |
| Chunking                      | ✅         |
| Embedding preparation         | ✅         |
| Semantic embeddings           | ✅         |
| Qdrant retrieval              | ✅         |
| Deterministic query expansion | ✅         |
| Prompt construction           | ✅         |
| Local LLM integration         | ✅         |
| FastAPI                       | ✅         |
| Swagger/OpenAPI               | ✅         |
| Streamlit UI                  | 🚧        |
| Docker                        | 🚧        |
| Kubernetes                    | 🚧        |
| GCP                           | 🔜        |
| Terraform                     | 🔜        |
| Retrieval evaluation          | 🔜        |
| Hybrid search                 | 🔜        |
| Reranking                     | 🔜        |
| Production observability      | 🔜        |

---

## Author / Project

**AI Based SIP Call Flow Analyser**

Built as an AI product architecture and development project exploring the application of RAG, semantic retrieval and LLMs to telecom/SIP troubleshooting.

```
Build → Measure → Learn → Architect → Improve
```
