# 🚀 Quick Start Guide

Get the AI Memory System Orchestrator running in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- At least one API key (OpenAI or Gemini)

---

## Step 1: Setup (2 minutes)

```bash
# Navigate to project
cd AI-Memory-Architecture

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure API Keys (1 minute)

Create `.env` file:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENAI_API_KEY=sk-proj-your-key-here
# OR
GEMINI_API_KEY=your-gemini-key-here
```

Get keys:
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://aistudio.google.com/app/apikey

---

## Step 3: Start Server (30 seconds)

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

---

## Step 4: Test It! (1 minute)

### Option A: Browser
Visit http://localhost:8000/docs and try the interactive API

### Option B: Test Script
Open a new terminal:
```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run tests
python tests/test_orchestrator.py
```

### Option C: cURL
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"test\", \"message\": \"Hi, I'm Sarah from Tokyo\"}"
```

---

## 🎉 You're Done!

The system is now running and ready to use.

### What You Can Do Now:

1. **Chat with Memory Context**
   ```bash
   POST /chat/
   ```

2. **Retrieve Memories**
   ```bash
   POST /chat/retrieve
   ```

3. **Check Health**
   ```bash
   GET /health
   ```

4. **View Metrics**
   ```bash
   GET /metrics
   ```

---

## 📖 Next Steps

- Read `README.md` for complete documentation
- Check `SETUP.md` for detailed setup instructions
- Review `orchestrator/README.md` for API details
- Explore interactive docs at http://localhost:8000/docs

---

## ⚠️ Troubleshooting

**Server won't start?**
- Check Python version: `python --version` (need 3.8+)
- Verify venv is activated: you should see `(venv)` in terminal
- Reinstall dependencies: `pip install -r requirements.txt`

**API key errors?**
- Check `.env` file exists and has valid keys
- Verify no extra spaces in API keys
- Try the other provider (OpenAI ↔ Gemini)

**Port 8000 in use?**
- Change port: `uvicorn orchestrator.main:app --port 8001`

---

## 💡 Quick Examples

### Example 1: First Conversation
```json
POST /chat/
{
  "user_id": "user123",
  "message": "Hi, I'm Sarah. I live in Tokyo and prefer email notifications."
}
```

### Example 2: Using Memory
```json
POST /chat/
{
  "user_id": "user123",
  "message": "What's my name and where do I live?"
}
```
Response will use stored memories!

### Example 3: Retrieve Memories
```json
POST /chat/retrieve
{
  "user_id": "user123",
  "query": "user preferences",
  "top_k": 5
}
```

---

**That's it! You're ready to build memory-augmented AI applications! 🎊**
