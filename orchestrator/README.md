# System Orchestrator - AI Memory Architecture

The System Orchestrator is the final layer that connects all components and provides a production-ready FastAPI backend for memory-augmented chat.

## Architecture

```
User Query → FastAPI Endpoint
    ↓
1. Retrieve relevant memories (MemoryEngine)
    ↓
2. Build context-aware prompt (PromptBuilder)
    ↓
3. Generate response (LLMClient - OpenAI/Gemini)
    ↓
4. Extract & store new memories (Background)
    ↓
5. Return response + metadata
```

## Components

### Services
- **ChatOrchestrator**: Main orchestration logic connecting all components
- **LLMClient**: Unified client for OpenAI and Gemini APIs
- **PromptBuilder**: Builds context-aware prompts with memory injection

### API Routes
- **POST /chat/**: Main chat endpoint with memory context
- **POST /chat/retrieve**: Retrieve memories without generating response
- **GET /health**: Health check for all components
- **GET /metrics**: Performance metrics and statistics

### Middleware
- **LoggingMiddleware**: Structured logging for all requests/responses

## Installation

1. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Running the Server

```bash
# From project root
python -m orchestrator.main

# Or with uvicorn directly
uvicorn orchestrator.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Usage Examples

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Hi, I'\''m Sarah from Tokyo. I prefer email notifications."
  }'
```

Response:
```json
{
  "response": "Hello Sarah! Nice to meet you...",
  "memories_used": 0,
  "latency_ms": 1250,
  "metadata": {
    "retrieval_ms": 45,
    "llm_ms": 1100,
    "extraction_ms": 105
  }
}
```

### Memory Retrieval

```bash
curl -X POST "http://localhost:8000/chat/retrieve" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "query": "user preferences",
    "top_k": 5
  }'
```

### Health Check

```bash
curl "http://localhost:8000/health"
```

### Metrics

```bash
curl "http://localhost:8000/metrics"
```

## Testing

Run the test suite:
```bash
# Start server first
python -m orchestrator.main

# In another terminal
python tests/test_orchestrator.py
```

## Performance Monitoring

The orchestrator tracks:
- **Total latency**: End-to-end response time
- **Memory retrieval time**: Time to fetch relevant memories
- **LLM inference time**: Time for LLM to generate response
- **Memory extraction time**: Time to extract and store new memories

Access metrics at `/metrics` endpoint.

## Configuration

Key parameters in `orchestrator/services/prompt_builder.py`:
- `MAX_MEMORIES = 5`: Maximum memories to inject in context
- `MAX_TOKENS_PER_MEMORY = 50`: Token budget per memory

Key parameters in `orchestrator/services/orchestrator.py`:
- `score_threshold = 0.3`: Minimum relevance score for memory retrieval
- `top_k = 5`: Number of memories to retrieve
- `temperature = 0.7`: LLM sampling temperature

## Error Handling

- Graceful degradation: System works even if memory retrieval fails
- LLM fallback: Tries OpenAI → Gemini → Fallback message
- Structured error responses with appropriate HTTP status codes

## Logging

All requests are logged with:
- Request ID
- Method and path
- Client IP
- Status code
- Latency
- Errors (if any)

Logs are in JSON format for easy parsing.
