# YouTube Video Analysis Agent - Step-by-Step Setup Guide

Welcome! This guide will walk you through setting up the YouTube Video Analysis Agent system locally using Ollama.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the System](#running-the-system)
4. [Testing](#testing)
5. [Troubleshooting](#troubleshooting)
6. [Next Steps](#next-steps)

---

## Prerequisites

### Required
- **macOS 10.13+**, **Linux**, or **Windows**
- **8GB+ RAM** (16GB recommended for better performance)
- **Python 3.9 or higher**
- **Internet connection** (to download models and transcripts)

### Check Your System

```bash
# Check Python version
python3 --version

# Check available RAM
# macOS
vm_stat | grep "Pages free"

# Linux
free -h

# Windows
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory
```

---

## Installation

### Step 1: Install Ollama

#### macOS
```bash
# Using Homebrew (recommended)
brew install ollama

# Or download from: https://ollama.ai
```

#### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

#### Windows
1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Follow the installation wizard

### Verify Installation
```bash
ollama --version
```

---

### Step 2: Start Ollama Service

Open a terminal and run:

```bash
ollama serve
```

You should see:
```
time=2024-01-15T10:30:00.123Z level=INFO msg="Listening on 127.0.0.1:11434"
```

**Keep this terminal open!** The Ollama service needs to keep running.

---

### Step 3: Download a Model

Open a **new terminal** and run:

```bash
# Download Mistral (recommended for quick start - 4GB)
ollama pull mistral
```

**Model Options:**

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **mistral** | 4GB | ⚡ Fast | ✓ Good | Quick start, balance |
| neural-chat | 4GB | ⚡ Fast | ✓ Good | Chat/conversation |
| llama2 | 7GB | 🟢 Medium | ✓✓ Excellent | Accuracy tasks |
| dolphin-mixtral | 26GB | 🐢 Slow | ✓✓✓ Excellent | Complex analysis |

For this guide, we recommend **mistral**.

### Verify Model Download
```bash
ollama list
```

You should see:
```
NAME            ID              SIZE    MODIFIED
mistral         2dfb...          4.1GB   2 minutes ago
```

---

### Step 4: Clone/Prepare the Project

Navigate to your projects directory:

```bash
cd /Users/viyangchaudhari/Projects/youtube
```

The project structure should look like:
```
youtube/
├── backend/
│   ├── src/
│   ├── requirements.txt
│   ├── .env
│   └── package.json
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── README.md
└── SETUP_GUIDE.md
```

---

### Step 5: Set Up Python Environment (Recommended)

Create a virtual environment:

```bash
cd /Users/viyangchaudhari/Projects/youtube/backend

# Create virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt.

---

### Step 6: Install Python Dependencies

```bash
# Make sure you're in the backend directory
cd /Users/viyangchaudhari/Projects/youtube/backend

# Install dependencies
pip install -r requirements.txt
```

This will install:
- `fastapi` - Web framework
- `ollama` - Ollama API client
- `yt-dlp` - YouTube transcript extraction
- `pydantic` - Data validation
- `chromadb` - Local storage
- And more...

**Installation time: 2-5 minutes**

---

### Step 7: Verify Installation

Test the connection to Ollama:

```bash
# Test Ollama API
curl http://localhost:11434/api/tags

# Should return something like:
# {"models":[{"name":"mistral:latest","modified_at":"2024-01-15T..."}]}
```

If you get a connection error, make sure `ollama serve` is running in another terminal.

---

## Running the System

### Option A: Run All Services (Recommended for First Time)

```bash
cd /Users/viyangchaudhari/Projects/youtube

# Make the script executable (one time)
chmod +x run.sh

# Run all services
./run.sh
```

This will start:
1. ✅ Backend API (port 8000)
2. ✅ Frontend server (port 8080)

### Option B: Run Services Manually

**Terminal 1 - Ollama Service** (should be running already)
```bash
ollama serve
```

**Terminal 2 - Backend API**
```bash
cd /Users/viyangchaudhari/Projects/youtube/backend

# Activate virtual environment (if created)
source venv/bin/activate

# Run the server
python src/main.py
```

You should see:
```
🎬 YouTube Video Analysis Agent System
==========================================

API Server starting...
Host: 0.0.0.0
Port: 8000

📚 Documentation: http://localhost:8000/docs
```

**Terminal 3 - Frontend Server**
```bash
cd /Users/viyangchaudhari/Projects/youtube/frontend

python -m http.server 8080
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/)
```

---

### Opening the Application

1. **Frontend UI:** Open your browser to http://localhost:8080
2. **API Documentation:** Open http://localhost:8000/docs

---

## Testing

### Test 1: Health Check API

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "ollama_connected": true,
  "model": "mistral"
}
```

### Test 2: Analyze a Sample Video

Using curl:
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

Or use the interactive API docs:
1. Go to http://localhost:8000/docs
2. Click on `/analyze` endpoint
3. Click "Try it out"
4. Enter a YouTube URL
5. Click "Execute"

### Test 3: Using the Web UI

1. Open http://localhost:8080
2. Paste a YouTube URL
3. Click "Analyze Video"
4. Wait for results (1-2 minutes)

**Sample URLs to try:**
- Tech talks: https://www.youtube.com/watch?v=...
- Tutorials: https://www.youtube.com/watch?v=...
- News: https://www.youtube.com/watch?v=...

---

## Troubleshooting

### Issue 1: "Connection refused: localhost:11434"

**Solution:**
```bash
# Make sure Ollama is running in a separate terminal
ollama serve
```

### Issue 2: "Model not found"

**Solution:**
```bash
# Pull the model
ollama pull mistral

# Verify it's available
ollama list
```

### Issue 3: Slow Analysis (> 2 minutes)

**Solutions:**
1. Use a faster model:
   ```bash
   ollama pull neural-chat
   # Update .env: OLLAMA_MODEL=neural-chat
   ```

2. Reduce transcript length (edit `backend/src/agents/summarizer.py`)

3. Increase system RAM or close other apps

### Issue 4: "No transcript available"

**Solution:**
- The video may have disabled captions
- Try another video
- Check if the URL is valid

### Issue 5: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Make sure you're in the backend directory
cd /Users/viyangchaudhari/Projects/youtube/backend

# Install dependencies again
pip install -r requirements.txt
```

### Issue 6: Cannot extract YouTube transcript

**Solution:**
- Some videos don't have captions enabled
- Try videos with auto-generated captions
- Use videos in English initially
- Check if the video URL is correct

---

## Project Architecture

### System Components

```
┌──────────────────────────────────────────────────────────┐
│                    YouTube URL Input                      │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│   Transcript Extraction Agent                            │
│   • Uses yt-dlp to fetch transcripts                     │
│   • Returns text with timestamps                         │
│   • Caches results for reuse                             │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│   Content Summarizer Agent                              │
│   • Generates 2-3 sentence summary                      │
│   • Creates 5-7 key bullet points                       │
│   • Extracts 3 key takeaways                            │
│   • Identifies main topics                              │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│   Insight Generator Agent                               │
│   • Identifies patterns                                 │
│   • Generates action items                              │
│   • Suggests related topics                             │
│   • Proposes follow-up questions                        │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│   Fact Checker Agent                                     │
│   • Validates claims against transcript                 │
│   • Generates confidence scores                         │
│   • Flags unsupported statements                        │
│   • Provides evidence citations                         │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│   Memory System (Local Storage)                         │
│   • Stores analysis history                             │
│   • Tracks user preferences                             │
│   • Enables video comparisons                           │
│   • Provides recommendations                            │
└──────────────────────────────────────────────────────────┘
```

### File Structure

```
backend/
├── src/
│   ├── agents/                    # Specialized agents
│   │   ├── transcript_extractor.py
│   │   ├── summarizer.py
│   │   ├── insight_generator.py
│   │   └── fact_checker.py
│   │
│   ├── memory/                    # Storage system
│   │   └── storage.py
│   │
│   ├── config.py                 # Configuration management
│   ├── guardrails.py             # Safety & validation
│   ├── orchestrator.py           # Coordinate all agents
│   └── main.py                   # FastAPI server
│
├── data/                         # Generated at runtime
│   ├── memory/                   # Analysis history
│   └── transcripts/              # Cached transcripts
│
├── requirements.txt              # Python dependencies
├── .env                          # Configuration
└── package.json                  # Package metadata

frontend/
├── index.html                    # UI structure
├── app.js                        # API interaction logic
└── style.css                     # Styling
```

---

## Next Steps

### 1. Basic Customization

Edit `backend/.env`:
```env
# Try a different model
OLLAMA_MODEL=neural-chat

# Increase/decrease analysis depth
MAX_TOKENS=3000

# Adjust response creativity
TEMPERATURE=0.5
```

### 2. Explore the API

Visit http://localhost:8000/docs to see:
- `/health` - System status
- `/analyze` - Analyze videos
- `/history` - View past analyses
- `/similar/{video_id}` - Find related videos

### 3. Build Custom Integrations

Add new features:
- Export summaries to PDF
- Email analysis results
- Slack integration
- Database backend (PostgreSQL)
- Advanced comparison tools

### 4. Deploy to Production

Options:
- Docker containerization
- AWS/Google Cloud deployment
- Build REST API for mobile apps
- Create browser extensions

---

## Performance Tips

1. **Start with Mistral model** - Best balance of speed and quality
2. **Use video caching** - Set `use_cache=true` in API requests
3. **Batch process videos** - Process multiple videos sequentially
4. **Increase timeout** - Some videos take 2-3 minutes
5. **Monitor system resources** - Keep task manager open

---

## Getting Help

### Check Logs

**Backend logs:**
```bash
# In terminal running backend API
# Logs appear automatically
```

**Ollama logs:**
```bash
# macOS
log stream --level debug --predicate 'process == "ollama"'

# Linux
journalctl -u ollama -f
```

### Common Solutions

| Problem | Solution |
|---------|----------|
| Ollama not responding | Restart: `ollama serve` |
| Model too slow | Switch to `mistral` or `neural-chat` |
| Out of memory | Close other apps, increase timeout |
| No transcripts | Ensure captions are enabled on video |
| API errors | Check browser console for errors |

---

## Success Checklist

- ✅ Ollama installed and running
- ✅ Model downloaded (`mistral`)
- ✅ Python 3.9+ installed
- ✅ Dependencies installed
- ✅ Backend API running (port 8000)
- ✅ Frontend server running (port 8080)
- ✅ Health check passing
- ✅ Successfully analyzed a YouTube video
- ✅ Results displaying in browser

---

## Congratulations! 🎉

You've successfully set up the YouTube Video Analysis Agent system. You can now:

1. ✅ Analyze YouTube videos
2. ✅ Generate intelligent summaries
3. ✅ Extract key insights
4. ✅ Validate facts with confidence scores
5. ✅ Store and reference past analyses

---

## Quick Reference Commands

```bash
# Start Ollama service
ollama serve

# List available models
ollama list

# Pull a new model
ollama pull neural-chat

# Test API connection
curl http://localhost:8000/health

# Analyze a video (replace URL)
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=..."}'

# View API documentation
open http://localhost:8000/docs

# Open web interface
open http://localhost:8080
```

---

## Support Resources

- **Ollama Docs:** https://ollama.ai
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **yt-dlp GitHub:** https://github.com/yt-dlp/yt-dlp
- **Project README:** See `README.md`

---

**Happy analyzing! 🚀**
