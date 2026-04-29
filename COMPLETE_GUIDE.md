# Complete Setup & Operation Guide
## YouTube Video Analysis Agent System with Ollama

---

## 📌 Executive Summary

This document provides a complete, step-by-step guide for setting up and running the YouTube Video Analysis Agent system locally using Ollama for local LLM inference.

**What you're building:**
- A multi-agent system that analyzes YouTube videos
- Generates summaries, insights, and validated facts
- Uses local models (no API keys needed)
- Stores analysis history for reference
- Includes a web interface and API

**Time to completion:** 30-45 minutes (including model download)

---

## 🎯 System Requirements

### Minimum
- CPU: Dual-core processor
- RAM: 8GB
- Storage: 20GB free
- Internet: Required initially for model download

### Recommended
- CPU: 4+ cores
- RAM: 16GB+
- Storage: 50GB free
- SSD preferred

### Operating Systems
- ✅ macOS 10.13+
- ✅ Linux (Ubuntu 20.04+, Fedora 33+, Debian 11+)
- ✅ Windows 10/11 with WSL2

---

## 🚀 Complete Setup Guide

### Phase 1: Install Core Tools (10-15 minutes)

#### 1.1 Install Ollama

**macOS:**
```bash
# Option 1: Using Homebrew (recommended)
brew install ollama

# Option 2: Direct download
# Visit https://ollama.ai and download the installer
```

**Linux (Ubuntu/Debian):**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
1. Download installer from https://ollama.ai
2. Run the installer
3. Follow the wizard
4. Restart your computer

**Verify installation:**
```bash
ollama --version
# Should output: ollama version X.X.X
```

#### 1.2 Start Ollama Service

This is critical - Ollama must be running as a background service.

```bash
ollama serve
```

**Expected output:**
```
time=2024-01-15T10:30:00.123Z level=INFO msg="Listening on 127.0.0.1:11434 (http)"
```

**Keep this terminal open!** This is your Ollama server.

#### 1.3 Download a Model (5-10 minutes)

Open a **new terminal** (keep the Ollama one running) and download a model:

```bash
ollama pull mistral
```

**What's happening:**
- Downloading a 4GB language model
- Storing it locally in `~/.ollama/models`
- This happens only once

**Verify download:**
```bash
ollama list
```

Output should show:
```
NAME            ID              SIZE    MODIFIED
mistral         2dfb7e6d4dbe    4.1GB   2 minutes ago
```

---

### Phase 2: Project Setup (5 minutes)

#### 2.1 Navigate to Project Directory

```bash
cd /Users/viyangchaudhari/Projects/youtube
```

Verify the structure:
```bash
ls -la
```

Should show: `backend/`, `frontend/`, `README.md`, etc.

#### 2.2 Set Up Python Virtual Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

#### 2.3 Install Python Dependencies

```bash
# Make sure you're in the backend directory with venv activated
pip install -r requirements.txt
```

**What's being installed:**
- `fastapi` - Web framework
- `ollama` - Python client for Ollama
- `yt-dlp` - YouTube transcript extraction
- `pydantic` - Data validation
- And 7+ more packages

**Installation time:** 2-5 minutes

**Verify installation:**
```bash
python -c "import fastapi; import ollama; print('✓ All packages installed')"
```

---

### Phase 3: Verification (5 minutes)

#### 3.1 Test Ollama Connection

```bash
# From any terminal (with venv activated)
cd /Users/viyangchaudhari/Projects/youtube/backend

python -c "
from src.config import config
if config.validate_ollama_connection():
    print('✓ Connected to Ollama')
else:
    print('✗ Cannot connect to Ollama')
"
```

#### 3.2 Run System Tests

```bash
cd /Users/viyangchaudhari/Projects/youtube
python test.py
```

Expected output:
```
============================================================
YouTube Video Analysis Agent - System Test
============================================================

🔧 Testing Configuration... ✓ PASSED
🔗 Testing Ollama Connection... ✓ PASSED
📝 Testing Transcript Extractor... ✓ PASSED
📋 Testing Content Summarizer... ✓ PASSED
💡 Testing Insight Generator... ✓ PASSED
✓ Testing Fact Checker... ✓ PASSED
💾 Testing Memory Storage... ✓ PASSED
🛡️  Testing Guardrails... ✓ PASSED
🎯 Testing Orchestrator... ✓ PASSED

============================================================
✅ ALL TESTS PASSED (9/9)
============================================================

🎉 Your system is ready!
```

---

## 🎬 Running the System

### Option A: Quick Start (Automated)

```bash
cd /Users/viyangchaudhari/Projects/youtube

chmod +x run.sh
./run.sh
```

This starts everything with one command.

### Option B: Manual Start (for Development)

**Terminal 1 - Ollama** (should already be running)
```bash
ollama serve
```

**Terminal 2 - Backend API**
```bash
cd /Users/viyangchaudhari/Projects/youtube/backend

# Activate venv
source venv/bin/activate

# Start server
python src/main.py
```

Expected output:
```
🎬 YouTube Video Analysis Agent System
==========================================

API Server starting...
Host: 0.0.0.0
Port: 8000

📚 Documentation: http://localhost:8000/docs
🔧 ReDoc: http://localhost:8000/redoc

Make sure Ollama is running:
  ollama serve
```

**Terminal 3 - Frontend**
```bash
cd /Users/viyangchaudhari/Projects/youtube/frontend

python -m http.server 8080
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

---

## 🌐 Accessing the System

### Web Interface
```
http://localhost:8080
```

Features:
- Paste YouTube URL
- View analysis results
- See analysis history
- Explore confidence metrics

### API Documentation
```
http://localhost:8000/docs
```

Features:
- Interactive API explorer
- Try endpoints live
- See response schemas
- Full endpoint documentation

### Direct API Calls

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Analyze Video:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=example",
    "use_cache": true
  }'
```

**View History:**
```bash
curl "http://localhost:8000/history?limit=10"
```

---

## 🎓 First Analysis

### Step-by-Step Guide

1. **Open the Web Interface**
   - Go to http://localhost:8080
   - You should see the analysis form

2. **Find a Test Video**
   - Use any YouTube video with captions
   - Example: Tech talks, tutorials, news videos

3. **Paste the URL**
   - Copy YouTube URL (from address bar or share button)
   - Paste into the input field

4. **Click "Analyze Video"**
   - System will:
     - Extract transcript (10-20 seconds)
     - Generate summary (30-60 seconds)
     - Create insights (30-60 seconds)
     - Check facts (10-30 seconds)
     - Display results (instant)

5. **View Results**
   - Short summary at top
   - Key bullet points
   - Deeper insights
   - Fact-checking results
   - Confidence scores

**Total time:** 2-3 minutes depending on video length

---

## 📊 Understanding the Output

### Summary Section
```
📋 Summary
├─ Short Summary (2-3 sentences)
├─ Key Points (5-7 bullets)
├─ Key Takeaways (3 main points)
└─ Topics (3-5 main topics covered)
```

### Insights Section
```
💡 Insights
├─ Patterns (recurring themes)
├─ Implications (consequences/impacts)
├─ Action Items (what to do)
├─ Related Topics (learn more about)
└─ Questions (follow-up questions)
```

### Fact Check Section
```
✓ Fact Check
├─ Support Percentage (% of claims supported)
├─ Average Confidence (0-100%)
├─ Detailed findings (each claim validated)
└─ Evidence (references to transcript)
```

### Quality Metrics
```
📊 Quality Metrics
├─ Overall Confidence (combined score)
└─ Claim Support % (validation percentage)
```

---

## ⚙️ Configuration

### Default Settings
Located in `backend/.env`:

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Model parameters
MAX_TOKENS=2000              # Increase for longer responses
TEMPERATURE=0.7              # 0=deterministic, 1=creative

# Memory
MEMORY_PATH=./data/memory    # Where to store analysis history

# Transcript caching
TRANSCRIPT_CACHE=./data/transcripts
```

### Customization Examples

**Faster Responses:**
```env
OLLAMA_MODEL=neural-chat
MAX_TOKENS=1000
TEMPERATURE=0.5
```

**Higher Quality:**
```env
OLLAMA_MODEL=llama2
MAX_TOKENS=3000
TEMPERATURE=0.3
```

**Save to New File:**
```bash
cp backend/.env backend/.env.custom
# Edit backend/.env.custom
# Update backend/src/config.py to load it
```

---

## 🔧 Troubleshooting

### Problem: Connection refused localhost:11434

**Cause:** Ollama service not running

**Solution:**
```bash
# In a terminal, make sure this is running:
ollama serve

# Then test connection:
curl http://localhost:11434/api/tags
```

### Problem: Model not found

**Cause:** Model wasn't downloaded

**Solution:**
```bash
ollama pull mistral
ollama list  # Verify it's there
```

### Problem: Analysis is very slow (> 3 minutes)

**Causes:**
1. Large model (llama2, dolphin-mixtral)
2. Long video (> 30 minutes)
3. Low system resources

**Solutions:**

Option 1: Switch to faster model
```bash
ollama pull neural-chat
# Edit backend/.env: OLLAMA_MODEL=neural-chat
```

Option 2: Reduce analysis depth
```env
# In backend/.env
MAX_TOKENS=1000        # Was 2000
TEMPERATURE=0.5        # Was 0.7
```

Option 3: Close other applications
- Free up RAM
- Reduce background processes

### Problem: No transcript available for video

**Cause:** Video doesn't have captions enabled

**Solution:**
- Try a different video
- Videos with auto-generated captions work
- English videos work best initially

**Test video sources:**
- TED Talks
- YouTube Learn
- Tech conference videos
- Educational channels

### Problem: Memory/Storage full

**Solution:**
```bash
# Clear transcript cache (keep analysis history)
rm -rf backend/data/transcripts/*

# Or clear everything
rm -rf backend/data/*
mkdir -p backend/data/memory backend/data/transcripts
```

### Problem: Python package conflicts

**Solution:**
```bash
# Reinstall in clean environment
rm -rf backend/venv
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

---

## 📈 Performance Optimization

### Model Selection for Speed

| Task | Recommended Model | Speed | Quality |
|------|-------------------|-------|---------|
| Quick analysis | mistral | ⚡⚡⚡ | ✓ |
| Balanced | neural-chat | ⚡⚡ | ✓✓ |
| High accuracy | llama2 | ⚡ | ✓✓✓ |
| Best quality | dolphin-mixtral | 🐢 | ✓✓✓✓ |

### Optimization Tips

1. **Use Mistral for development**
   ```env
   OLLAMA_MODEL=mistral
   ```

2. **Enable transcript caching**
   - Set `use_cache=true` in API requests
   - Saves time on repeated videos

3. **Reduce model parameters**
   ```env
   MAX_TOKENS=1500
   TEMPERATURE=0.5
   ```

4. **Batch operations**
   - Process multiple videos sequentially
   - Don't run in parallel (resource intensive)

5. **Monitor system resources**
   - Keep Task Manager/Activity Monitor open
   - Watch RAM and CPU usage
   - Close other apps if needed

---

## 🔒 Security & Best Practices

### API Security
- API runs on localhost only (development)
- No authentication (local use)
- For production, add authentication

### Data Privacy
- All data stored locally
- No external API calls (except YouTube)
- Transcript caching is optional

### Model Security
- Models downloaded from Ollama registry
- Runs locally (no cloud processing)
- You maintain full control

### Backup & Recovery
```bash
# Backup analysis history
cp -r backend/data/memory ~/backup_youtube_analysis

# Restore if needed
cp -r ~/backup_youtube_analysis/* backend/data/memory/
```

---

## 📚 API Reference

### Endpoints

**POST /analyze**
```json
Request:
{
  "url": "https://www.youtube.com/watch?v=...",
  "use_cache": true
}

Response:
{
  "status": "success",
  "data": {
    "metadata": {...},
    "summary": {...},
    "insights": {...},
    "fact_check": {...},
    "quality_metrics": {...}
  }
}
```

**GET /health**
```json
Response:
{
  "status": "healthy",
  "ollama_connected": true,
  "model": "mistral"
}
```

**GET /history**
```json
Response:
{
  "status": "success",
  "count": 5,
  "data": [...]
}
```

**GET /similar/{video_id}**
```json
Response:
{
  "status": "success",
  "count": 3,
  "data": [...]
}
```

**GET /config**
```json
Response:
{
  "ollama_url": "http://localhost:11434",
  "model": "mistral",
  "max_tokens": 2000,
  "temperature": 0.7,
  "memory_path": "./data/memory",
  "transcript_cache": "./data/transcripts"
}
```

---

## 🧪 Testing & Validation

### Manual Testing Checklist

- [ ] Ollama service running
- [ ] Model downloaded (`ollama list` shows mistral)
- [ ] Python dependencies installed
- [ ] Backend API starts without errors
- [ ] Frontend loads at localhost:8080
- [ ] API health check returns true
- [ ] Can analyze a sample video
- [ ] Results display correctly
- [ ] Confidence scores show

### Automated Testing

```bash
cd /Users/viyangchaudhari/Projects/youtube
python test.py
```

All tests should pass with ✓ marks.

---

## 🎓 Learning Resources

### Understanding the System

**Multi-Agent Architecture:**
- Each agent specializes in one task
- Agents pass structured data between them
- Orchestrator coordinates the pipeline

**LLM Basics:**
- Models: Language patterns learned from data
- Prompting: How to ask the model for specific outputs
- Tokens: Words/chunks the model processes

**Local LLMs with Ollama:**
- Models run on your machine
- No internet needed after download
- Complete privacy and control

### Next Steps

1. **Experiment with different models**
   ```bash
   ollama pull neural-chat
   # Update .env and test
   ```

2. **Analyze different video types**
   - Tech talks
   - Tutorials
   - News videos
   - Documentaries

3. **Explore the API**
   - Build your own tools
   - Integrate with other services
   - Create batch analysis scripts

4. **Customize prompts**
   - Edit `summarizer.py` prompts
   - Adjust output formats
   - Add custom instructions

---

## 📞 Support & Help

### Getting Help

1. **Check the troubleshooting section** above
2. **Review QUICKSTART.md** for quick reference
3. **Check API documentation** at localhost:8000/docs
4. **Review code comments** in source files

### Common Issues Quick Fixes

```bash
# Ollama not responding
ollama serve

# Model not found
ollama pull mistral

# Python packages missing
pip install -r requirements.txt

# Connection refused
curl http://localhost:11434/api/tags

# API won't start
python src/main.py
# Check error message for details
```

### Logs & Debugging

```bash
# Backend API logs appear in terminal
# Watch for error messages

# Check Ollama
ollama list          # List models
ollama show mistral  # Show model details

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/config
```

---

## 🎉 Success Indicators

You'll know everything is working when:

✅ **Ollama Service**
- `ollama serve` runs without errors
- `curl http://localhost:11434/api/tags` returns model list

✅ **Python Environment**
- `source venv/bin/activate` shows `(venv)` in prompt
- `python test.py` passes all 9 tests

✅ **Backend API**
- `python src/main.py` starts on port 8000
- `curl http://localhost:8000/health` returns healthy

✅ **Frontend**
- http://localhost:8080 loads with form
- Can paste YouTube URL and click analyze

✅ **Analysis**
- Video analysis completes in 1-3 minutes
- Results display correctly
- Confidence scores show (0-100%)

✅ **Memory**
- Previous analyses appear in history
- Can load past analyses

---

## 🚀 What's Next?

### Immediate (Today)
- ✅ Complete this guide
- ✅ Analyze 5-10 videos
- ✅ Get comfortable with the interface

### Short-term (This Week)
- Experiment with different models
- Try different video types
- Explore the API

### Medium-term (This Month)
- Customize prompts
- Integrate with other tools
- Build analysis utilities

### Long-term (Production)
- Add database backend
- Deploy to cloud
- Build mobile app
- Add advanced features

---

## 📝 Summary

You now have a fully functional YouTube Video Analysis Agent system that:

1. ✅ Extracts transcripts from YouTube videos
2. ✅ Generates intelligent summaries
3. ✅ Creates deeper insights
4. ✅ Validates facts with confidence scores
5. ✅ Stores analysis history
6. ✅ Provides a web interface and API
7. ✅ Uses local LLMs (complete privacy)
8. ✅ Requires no API keys

**Total setup time:** 30-45 minutes
**Running cost:** $0 (local processing)
**Learning value:** Extremely high (understand multi-agent systems, LLMs, and more)

---

**Congratulations and happy analyzing! 🎬🚀**

For quick reference, see:
- `QUICKSTART.md` - Fast startup guide
- `README.md` - Project overview
- `backend/` - Source code with comments
- `frontend/` - Web interface code

---

*Last updated: 2024 | YouTube Video Analysis Agent System | Powered by Ollama*
