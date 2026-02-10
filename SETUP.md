# Setup Guide - AI Memory Architecture

Complete step-by-step guide to get the system running.

## Prerequisites

- Python 3.8+ installed
- pip package manager
- OpenAI API key OR Google Gemini API key (at least one)

## Step-by-Step Setup

### 1. Clone/Download the Project

```bash
cd AI-Memory-Architecture
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI & uvicorn (API server)
- OpenAI & Google Gemini clients
- FAISS (vector search)
- sentence-transformers (embeddings)
- Other dependencies

**Note:** Installation may take 5-10 minutes due to ML libraries.

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
# Windows
type nul > .env

# Linux/Mac
touch .env
```

Edit `.env` and add your API keys:

```env
# At least one of these is required
OPENAI_API_KEY=sk-proj-your-key-here
GEMINI_API_KEY=your-gemini-key-here
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://aistudio.google.com/app/apikey

### 5. Verify Installation

Test that everything is installed correctly:

```bash
python -c "import fastapi, openai, faiss, sentence_transformers; print('✅ All dependencies installed!')"
```

### 6. Run the Server

```bash
python run_orchestrator.py
```

You should see:
```
🚀 Starting AI Memory System Orchestrator
📍 Server will be available at:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
```

### 7. Test the API

Open a new terminal and run:

```bash
python tests/test_orchestrator.py
```

Or visit in your browser:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Quick Test with cURL

```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"test123\", \"message\": \"Hi, I'm Sarah from Tokyo\"}"
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "API key not found" or LLM errors

**Solution:** Check your `.env` file:
```bash
# View .env contents (Windows)
type .env

# View .env contents (Linux/Mac)
cat .env
```

Make sure at least one API key is set correctly.

### Issue: Port 8000 already in use

**Solution:** Use a different port:
```bash
uvicorn orchestrator.main:app --port 8001
```

### Issue: FAISS installation fails

**Solution:** Install FAISS separately:
```bash
pip install faiss-cpu --no-cache-dir
```

### Issue: Slow first request

**Solution:** This is normal! The first request loads the embedding model (~80MB). Subsequent requests will be much faster.

## Development Mode

Run with auto-reload for development:

```bash
uvicorn orchestrator.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production, consider:

1. **Use a production ASGI server:**
```bash
pip install gunicorn
gunicorn orchestrator.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Set environment variables:**
```bash
export ENVIRONMENT=production
export LOG_LEVEL=warning
```

3. **Configure CORS properly** in `orchestrator/main.py`

4. **Add authentication middleware**

5. **Use a reverse proxy** (nginx, Caddy)

## Next Steps

1. ✅ Server is running
2. 📖 Read the API docs at http://localhost:8000/docs
3. 🧪 Run tests: `python tests/test_orchestrator.py`
4. 🎯 Try the demo: `python tests/demo_memory_flow.py`
5. 🚀 Build your application using the API!

## Need Help?

- Check the main README.md for architecture details
- Review orchestrator/README.md for API documentation
- Open an issue on GitHub

---

Happy coding! 🎉
