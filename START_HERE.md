# 🎬 YouTube Video Analysis Agent - Getting Started

## What You're Building

A multi-agent AI system that:
- Analyzes YouTube videos intelligently
- Generates summaries and key insights
- Validates facts with confidence scores
- Uses local models (complete privacy, no API keys)
- Stores and tracks analysis history

## ⏱️ Time Estimate: 30-45 minutes

---

## 📋 Quick Setup

### Step 1: Install Ollama (5 minutes)

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai

### Step 2: Start Ollama Service (Keep Running)

```bash
ollama serve
```

### Step 3: Download Model (In New Terminal, 5-10 min)

```bash
ollama pull mistral
```

### Step 4: Navigate to Project

```bash
cd /Users/viyangchaudhari/Projects/youtube
```

### Step 5: Set Up Python (5 minutes)

```bash
cd backend

# Create environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 6: Run Tests (1 minute)

```bash
cd ..
python test.py
```

Should show: `✅ ALL TESTS PASSED (9/9)`

---

## 🚀 Running the System

### Option A: Automated (One Command)

```bash
./run.sh
```

### Option B: Manual (3 Terminals)

**Terminal 1 - Ollama** (should already be running)
```bash
ollama serve
```

**Terminal 2 - Backend API**
```bash
cd backend
source venv/bin/activate
python src/main.py
```

**Terminal 3 - Frontend**
```bash
cd frontend
python -m http.server 8080
```

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Web Interface** | http://localhost:8080 | Upload & analyze videos |
| **API Docs** | http://localhost:8000/docs | Interactive API explorer |
| **API Endpoint** | http://localhost:8000/analyze | Direct API access |

---

## 📝 First Analysis

1. Go to http://localhost:8080
2. Paste a YouTube URL
3. Click "Analyze Video"
4. Wait 2-3 minutes
5. View results with confidence scores

**Sample videos to try:**
- TED Talks
- YouTube Learn videos
- Tech conference talks
- Educational content

---

## 📊 What You Get

```
Results Include:
├─ Summary
│  ├─ 2-3 sentence overview
│  ├─ 5-7 key bullet points
│  ├─ 3 main takeaways
│  └─ Main topics covered
│
├─ Insights
│  ├─ Patterns identified
│  ├─ Actionable items
│  ├─ Related topics
│  └─ Follow-up questions
│
├─ Fact Checking
│  ├─ % of claims supported
│  ├─ Confidence scores
│  └─ Evidence citations
│
└─ Quality Metrics
   ├─ Overall confidence (0-100%)
   └─ Support percentage
```

---

## ⚙️ Configuration

Edit `backend/.env`:

```env
# Model to use
OLLAMA_MODEL=mistral      # Fast and good quality

# Adjust for speed vs quality
MAX_TOKENS=2000           # Reduce for speed
TEMPERATURE=0.7           # 0=deterministic, 1=creative

# Output paths
MEMORY_PATH=./data/memory
TRANSCRIPT_CACHE=./data/transcripts
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused localhost:11434" | Make sure `ollama serve` is running |
| "Model not found" | Run `ollama pull mistral` |
| API won't start | Check if port 8000 is in use |
| Frontend won't load | Check if port 8080 is in use |
| Analysis very slow | Switch to mistral or reduce MAX_TOKENS |
| No transcript available | Video may not have captions |

---

## 📚 Understanding the Architecture

### Multi-Agent Pipeline

```
YouTube URL
    ↓
[Transcript Extractor]  ← Gets video text
    ↓
[Summarizer]            ← Creates summaries
    ↓
[Insight Generator]     ← Finds patterns
    ↓
[Fact Checker]          ← Validates claims
    ↓
[Memory Storage]        ← Saves results
    ↓
Results (JSON)
```

### Key Components

1. **Transcript Extractor**
   - Uses yt-dlp to fetch video captions
   - Extracts text with timestamps
   - Caches for reuse

2. **Summarizer**
   - Generates 2-3 sentence summary
   - Creates 5-7 key bullets
   - Identifies main topics

3. **Insight Generator**
   - Finds patterns
   - Generates action items
   - Proposes related topics

4. **Fact Checker**
   - Validates each claim
   - Confidence scoring
   - Links to evidence

5. **Memory System**
   - Stores analysis history
   - Enables comparisons
   - Finds similar videos

---

## 🎓 Learning Path

### Week 1: Setup & Experimentation
- ✅ Complete this guide
- Analyze 5-10 videos
- Explore the API
- Get comfortable with the interface

### Week 2: Customization
- Try different models
- Adjust prompts
- Experiment with parameters
- Build test utilities

### Week 3: Integration
- Integrate with other tools
- Build custom workflows
- Explore batch processing
- Create advanced features

---

## 📖 More Documentation

- **QUICKSTART.md** - Fast reference guide
- **COMPLETE_GUIDE.md** - Detailed setup instructions
- **README.md** - Project overview and API reference
- **SETUP_GUIDE.md** - Architecture details

---

## 🔗 Quick Commands

```bash
# Verify Ollama connection
curl http://localhost:11434/api/tags

# Health check
curl http://localhost:8000/health

# Analyze video (replace URL)
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=..."}'

# View analysis history
curl http://localhost:8000/history

# List available models
ollama list

# Pull another model
ollama pull neural-chat
```

---

## ✅ Success Checklist

Before starting, make sure you have:

- [ ] Ollama installed (`ollama --version`)
- [ ] Ollama service running (`ollama serve`)
- [ ] Model downloaded (`ollama list` shows mistral)
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Project directory ready
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Tests passing (`python test.py`)

---

## 🎯 Next Steps

1. **Right Now:**
   ```bash
   cd /Users/viyangchaudhari/Projects/youtube
   python test.py
   ```

2. **Then Start Services:**
   ```bash
   ./run.sh
   ```

3. **Finally Open Browser:**
   - http://localhost:8080

---

## 📞 Need Help?

**Connection Issues:**
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, verify
curl http://localhost:11434/api/tags
```

**Python Issues:**
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

**API Issues:**
```bash
# Check API is running
curl http://localhost:8000/health
```

---

## 🎉 You're All Set!

Your YouTube Video Analysis Agent is ready to:
- ✅ Extract and analyze video content
- ✅ Generate intelligent insights
- ✅ Validate facts and build confidence scores
- ✅ Store and reference past analyses
- ✅ Provide a full-featured API

**Enjoy analyzing! 🚀**

---

## 📊 Model Options

Start with **mistral** for best experience:

```bash
# Fast (recommended to start)
ollama pull mistral

# Balanced
ollama pull neural-chat

# High quality (slower)
ollama pull llama2

# Best quality (very slow)
ollama pull dolphin-mixtral
```

To switch models, edit `backend/.env`:
```env
OLLAMA_MODEL=neural-chat
```

---

## 🔐 Privacy & Security

✅ All processing happens locally  
✅ No data sent to external services  
✅ No API keys needed  
✅ Complete privacy  
✅ You control your data  

---

*Built with ❤️ using Ollama, LangChain, and FastAPI*

**Ready? Let's go! 🎬**
