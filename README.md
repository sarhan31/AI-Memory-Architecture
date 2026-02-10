# AI Memory Architecture

A production-ready long-term memory system for AI assistants that extracts, stores, and retrieves structured user information from conversations using semantic search and LLM-powered extraction.

## 🎯 Overview

This system enables AI assistants to maintain persistent memory across conversations by:
- **Extracting** structured memories from natural language conversations
- **Storing** memories with semantic embeddings for efficient retrieval
- **Retrieving** relevant context based on user queries
- **Orchestrating** memory-augmented chat responses via FastAPI

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    System Orchestrator                       │
│                      (FastAPI Layer)                         │
│  • Chat endpoint with memory context                         │
│  • Prompt injection & LLM inference                          │
│  • Latency monitoring & metrics                              │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│                    Memory Manager                            │
│  • MemoryEngine: Storage & retrieval                         │
│  • VectorStore: FAISS-based semantic search                  │
│  • Embedding Service: sentence-transformers                  │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│                    Memory Extractor                          │
│  • LLM-based extraction (OpenAI/Gemini)                      │
│  • Structured JSON output with validation                    │
│  • Fallback to rule-based extraction                         │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Components

### 1. Memory Extractor (`extractor/`)
- Processes conversations using LLMs (OpenAI GPT-4o-mini or Google Gemini)
- Extracts structured memories following strict JSON schemas
- Categorizes into: preferences, facts, constraints, commitments

### 2. Memory Manager (`memory_manager/`)
- **MemoryEngine**: Core storage and retrieval logic
- **VectorStore**: FAISS-based vector database for semantic search
- **Embedding Service**: Local embeddings using sentence-transformers
- Handles add/update/merge operations with deduplication

### 3. System Orchestrator (`orchestrator/`) ⭐ NEW
- **FastAPI Backend**: Production-ready REST API
- **ChatOrchestrator**: Connects all components
- **LLMClient**: Unified client for OpenAI and Gemini
- **PromptBuilder**: Context-aware prompt construction
- **Logging & Metrics**: Performance monitoring

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### 3. Run the Orchestrator

```bash
# Quick start
python run_orchestrator.py

# Or manually
python -m orchestrator.main
```

Server starts at: `http://localhost:8000`

API Docs: `http://localhost:8000/docs`

## 📡 API Endpoints

### Chat with Memory Context
```bash
POST /chat/
{
  "user_id": "user123",
  "message": "Hi, I'm Sarah from Tokyo. I prefer email notifications."
}
```

Response:
```json
{
  "response": "Hello Sarah! Nice to meet you...",
  "memories_used": 3,
  "latency_ms": 1250,
  "metadata": {
    "retrieval_ms": 45,
    "llm_ms": 1100,
    "extraction_ms": 105
  }
}
```

### Retrieve Memories
```bash
POST /chat/retrieve
{
  "user_id": "user123",
  "query": "user preferences",
  "top_k": 5
}
```

### Health Check
```bash
GET /health
```

### Performance Metrics
```bash
GET /metrics
```

## 🧪 Testing

### Test the Orchestrator API
```bash
# Start server
python run_orchestrator.py

# In another terminal, run tests
python tests/test_orchestrator.py
```

### Test Memory Engine
```bash
python tests/test_memory_engine.py
```

### Test Memory Flow
```bash
python tests/demo_memory_flow.py
```

## 📊 Memory Types

The system categorizes memories into 4 types:

### Preferences
- preferred_language, communication_style, timezone
- call_time_preference, contact_method, notification_preference

### Facts
- user_name, location, occupation
- education, company, device_used

### Constraints
- no_calls_time_range, do_not_contact_days
- dietary_restriction, access_limitation, budget_limit

### Commitments
- reminder_request, scheduled_call
- task_deadline, follow_up_request

## 🔧 Configuration

### Memory Retrieval
- `top_k = 5`: Number of memories to retrieve
- `score_threshold = 0.3`: Minimum relevance score
- `MAX_MEMORIES = 5`: Maximum memories in context

### LLM Settings
- `temperature = 0.7`: Sampling temperature
- `model = "gpt-4o-mini"`: OpenAI model
- `model = "gemini-2.0-flash"`: Gemini model

## 📈 Performance

Typical latencies:
- Memory retrieval: ~50ms
- LLM inference: ~1000-1500ms
- Memory extraction: ~100-200ms
- **Total end-to-end: ~1.2-2.0s**

## 🛠️ Tech Stack

- **FastAPI**: REST API framework
- **OpenAI / Gemini**: LLM providers
- **FAISS**: Vector similarity search
- **sentence-transformers**: Local embeddings
- **Pydantic**: Data validation
- **uvicorn**: ASGI server

## 📁 Project Structure

```
AI-Memory-Architecture/
├── orchestrator/           # FastAPI orchestration layer
│   ├── api/
│   │   ├── routes/        # API endpoints
│   │   └── models/        # Request/response models
│   ├── services/          # Core services
│   │   ├── orchestrator.py
│   │   ├── llm_client.py
│   │   └── prompt_builder.py
│   └── middleware/        # Logging middleware
├── memory_manager/        # Memory storage & retrieval
│   ├── memory_engine.py
│   ├── vector_store.py
│   └── embedding_service.py
├── extractor/             # Memory extraction
│   └── extract_memory.py
├── prompts/               # LLM prompts
├── schema/                # JSON schemas
├── tests/                 # Test scripts
└── run_orchestrator.py    # Quick start script
```

## 🔐 Security Notes

- Store API keys in `.env` file (never commit)
- Configure CORS appropriately for production
- Implement authentication for production use
- Rate limit API endpoints

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ for memory-augmented AI systems**
