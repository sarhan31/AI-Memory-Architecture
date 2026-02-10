# 🏠 Local Setup Guide (No API Keys Required)

Run the AI Memory System completely locally without OpenAI or Gemini!

## 🎯 Local Options

### Option 1: Rule-Based Fallback (Simplest)
✅ **No installation needed**
✅ **Works immediately**
✅ **No API keys required**
⚠️ Limited conversational ability (rule-based responses)

### Option 2: Ollama (Recommended for Local)
✅ **Fully local LLM**
✅ **No API keys required**
✅ **Good conversational ability**
⚠️ Requires ~4GB disk space and installation

---

## 🚀 Quick Start (Rule-Based Fallback)

### 1. Setup Environment

```bash
# Navigate to project
cd AI-Memory-Architecture

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies (without OpenAI/Gemini)
pip install python-dotenv faiss-cpu numpy sentence-transformers fastapi uvicorn[standard] pydantic python-multipart httpx requests
```

### 2. Configure for Local Mode

The `.env` file is already configured for local mode:

```env
USE_LOCAL_FALLBACK=true
```

### 3. Start Server

```bash
python run_orchestrator.py
```

You should see:
```
🚀 Starting AI Memory System Orchestrator
[LLMClient] Using local fallback (rule-based)
📍 Server will be available at:
   - API: http://localhost:8000
```

### 4. Test It!

```bash
# In another terminal
python tests/test_orchestrator.py
```

---

## 🦙 Option 2: Using Ollama (Better Responses)

### 1. Install Ollama

**Windows/Mac/Linux:**
Visit https://ollama.ai and download the installer

Or use command line:
```bash
# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Mac
brew install ollama
```

### 2. Download a Model

```bash
# Start Ollama service (if not auto-started)
ollama serve

# In another terminal, pull a model
ollama pull llama2

# Or try other models:
# ollama pull mistral
# ollama pull phi
# ollama pull codellama
```

### 3. Configure .env

Edit `.env`:
```env
USE_LOCAL_FALLBACK=true
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### 4. Start Server

```bash
python run_orchestrator.py
```

You should see:
```
[LLMClient] Ollama detected at http://localhost:11434
🚀 Starting AI Memory System Orchestrator
```

---

## 🧪 Testing Local Mode

### Test with cURL

```bash
# Test health
curl http://localhost:8000/health

# Test chat (rule-based)
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"test\", \"message\": \"Hi, I'm Sarah from Tokyo\"}"
```

Expected response (rule-based):
```json
{
  "response": "Hello Sarah! Nice to meet you! It's great to connect with someone from Tokyo. How can I help you today?",
  "memories_used": 0,
  "latency_ms": 50,
  "metadata": {...}
}
```

### Test Memory Functionality

```bash
# First message (stores memory)
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"user123\", \"message\": \"Hi, I'm Sarah. I prefer email notifications.\"}"

# Second message (uses stored memory)
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"user123\", \"message\": \"What are my preferences?\"}"
```

The second response will include `"memories_used": 1` showing it retrieved your preference!

---

## 📊 Comparison of Local Options

| Feature | Rule-Based | Ollama | OpenAI/Gemini |
|---------|-----------|--------|---------------|
| **Setup Time** | Instant | 10 min | 5 min |
| **Cost** | Free | Free | Paid |
| **Internet Required** | No | No | Yes |
| **Response Quality** | Basic | Good | Excellent |
| **Speed** | Very Fast | Fast | Medium |
| **Disk Space** | ~500MB | ~4GB | ~500MB |
| **Memory Works** | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🎯 What Works in Local Mode

✅ **Memory Storage** - Fully functional
✅ **Memory Retrieval** - Semantic search works perfectly
✅ **Memory Extraction** - Uses rule-based extraction
✅ **Vector Search** - FAISS works locally
✅ **API Endpoints** - All endpoints functional
✅ **Health Checks** - Full monitoring
✅ **Metrics** - Performance tracking

⚠️ **Limited** - Conversational responses (rule-based is simple)

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors

```bash
# Make sure you're in the venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install core dependencies
pip install -r requirements.txt
```

### Issue: Ollama not detected

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama
ollama serve
```

### Issue: Slow first request

This is normal! The first request loads the embedding model (~80MB). Subsequent requests are much faster.

---

## 🚀 Performance in Local Mode

### Rule-Based Fallback
- Memory retrieval: ~50ms
- Response generation: ~5ms (instant!)
- Memory extraction: ~10ms (rule-based)
- **Total: ~65ms** ⚡ Very fast!

### Ollama (llama2)
- Memory retrieval: ~50ms
- Response generation: ~500-2000ms (depends on hardware)
- Memory extraction: ~500ms
- **Total: ~1-2.5s** 🚀 Good!

---

## 💡 Tips for Local Mode

1. **Rule-based is great for testing** - Fast and reliable
2. **Ollama for better conversations** - Worth the setup
3. **Memory features work perfectly** - No compromise on core functionality
4. **Combine with cloud later** - Easy to add API keys later

---

## 🎓 Next Steps

1. ✅ Server running locally
2. 🧪 Test with `python tests/test_orchestrator.py`
3. 📖 Check API docs at http://localhost:8000/docs
4. 🚀 Build your application!

---

## 🔄 Switching to Cloud Later

To add cloud LLMs later, just edit `.env`:

```env
# Add OpenAI
OPENAI_API_KEY=sk-proj-your-key-here

# Or add Gemini
GEMINI_API_KEY=your-gemini-key-here

# Keep local fallback as backup
USE_LOCAL_FALLBACK=true
```

The system will automatically use cloud LLMs when available!

---

**Enjoy your fully local AI Memory System! 🎉**
