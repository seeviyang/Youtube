# Project Structure & File Overview

## 📁 Complete Directory Structure

```
youtube/
│
├── 📄 Documentation
│   ├── START_HERE.md              ← Begin here! Quick guide (3 min read)
│   ├── QUICKSTART.md              ← Setup instructions (15 min)
│   ├── COMPLETE_GUIDE.md          ← Detailed guide (30 min read)
│   ├── SETUP_GUIDE.md             ← Architecture deep-dive
│   └── README.md                  ← Project overview & API reference
│
├── 🔧 Setup & Run Scripts
│   ├── quickstart.sh              ← Verify dependencies & download models
│   ├── run.sh                     ← Start all services (1 command)
│   └── test.py                    ← System verification tests
│
├── 📘 Backend API
│   ├── backend/
│   │   ├── 📦 src/                # Source code
│   │   │   ├── __init__.py        # Package initialization
│   │   │   ├── config.py          # Configuration & settings
│   │   │   ├── guardrails.py      # Safety & validation
│   │   │   ├── orchestrator.py    # Main orchestrator
│   │   │   ├── main.py            # FastAPI server
│   │   │   │
│   │   │   ├── agents/            # Specialized agents
│   │   │   │   ├── __init__.py
│   │   │   │   ├── transcript_extractor.py   # YouTube → Text
│   │   │   │   ├── summarizer.py             # Text → Summary
│   │   │   │   ├── insight_generator.py      # Summary → Insights
│   │   │   │   └── fact_checker.py           # Insights → Validated
│   │   │   │
│   │   │   └── memory/            # Storage system
│   │   │       ├── __init__.py
│   │   │       └── storage.py     # History & preferences
│   │   │
│   │   ├── 📁 data/               # Generated at runtime
│   │   │   ├── memory/            # Analysis history (JSON)
│   │   │   └── transcripts/       # Cached transcripts
│   │   │
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── .env                   # Configuration
│   │   ├── package.json           # Package metadata
│   │   ├── tsconfig.json          # TypeScript config
│   │   └── venv/                  # Virtual environment (created)
│   │
│   └── This is the core API server
│
├── 🌐 Frontend Web UI
│   ├── frontend/
│   │   ├── index.html             # Main UI structure
│   │   ├── app.js                 # Client-side logic
│   │   ├── style.css              # Styling
│   │   └── README.md              # Frontend docs (optional)
│   │
│   └── Provides visual interface for analysis
│
└── 📊 Project Files
    ├── This file (you are here!)
    ├── README.md
    ├── QUICKSTART.md
    ├── COMPLETE_GUIDE.md
    └── START_HERE.md
```

---

## 📄 Key Files Explained

### Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| `START_HERE.md` | Quick intro & setup checklist | 3 min |
| `QUICKSTART.md` | Step-by-step setup guide | 15 min |
| `COMPLETE_GUIDE.md` | Comprehensive setup & operation | 30 min |
| `SETUP_GUIDE.md` | Architecture & technical details | 20 min |
| `README.md` | Project overview & API reference | 10 min |

### Backend Source Code

| File | Purpose | Key Classes |
|------|---------|-------------|
| `config.py` | Configuration management | `Config` |
| `guardrails.py` | Safety & validation | `OutputGuardrails`, `ContentFilter` |
| `orchestrator.py` | Main system orchestrator | `VideoAnalysisOrchestrator` |
| `main.py` | FastAPI server | FastAPI app |
| `agents/transcript_extractor.py` | Extract YouTube transcripts | `TranscriptExtractor` |
| `agents/summarizer.py` | Generate summaries | `ContentSummarizer` |
| `agents/insight_generator.py` | Create insights | `InsightGenerator` |
| `agents/fact_checker.py` | Validate claims | `FactChecker` |
| `memory/storage.py` | Store analysis history | `MemoryStorage` |

### Configuration Files

| File | Purpose |
|------|---------|
| `backend/.env` | Runtime configuration (Ollama URL, model, etc.) |
| `backend/requirements.txt` | Python package dependencies |
| `backend/package.json` | Package metadata |
| `backend/tsconfig.json` | TypeScript config (optional) |

### Frontend Files

| File | Purpose |
|------|---------|
| `frontend/index.html` | HTML structure & layout |
| `frontend/app.js` | JavaScript for API interaction |
| `frontend/style.css` | CSS styling |

---

## 🔄 Data Flow

### Request Path
```
User Input (URL)
         ↓
   Frontend UI
         ↓
   /analyze API
         ↓
  Orchestrator
         ↓
 Transcript Extractor
         ↓
   Summarizer
         ↓
 Insight Generator
         ↓
   Fact Checker
         ↓
  Memory Storage
         ↓
  JSON Response
         ↓
 Display Results
```

### File Generation
```
During Analysis:
youtube/backend/data/
├── transcripts/
│   ├── {hash1}.json      ← Cached transcript 1
│   ├── {hash2}.json      ← Cached transcript 2
│   └── ...
│
└── memory/
    ├── history.json      ← All analyses (appended)
    └── preferences.json  ← User settings (updated)
```

---

## 🚀 How to Use Each Component

### Run the Test Suite
```bash
cd /Users/viyangchaudhari/Projects/youtube
python test.py
```

### Run Quickstart Setup
```bash
cd /Users/viyangchaudhari/Projects/youtube
chmod +x quickstart.sh
./quickstart.sh
```

### Run All Services
```bash
cd /Users/viyangchaudhari/Projects/youtube
chmod +x run.sh
./run.sh
```

### Access the System

**Web Interface:**
- URL: http://localhost:8080
- File: `frontend/index.html` + `frontend/app.js`

**API Documentation:**
- URL: http://localhost:8000/docs
- Generated from `backend/src/main.py`

**Direct API:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=..."}'
```

---

## 📦 Dependencies

### Python Packages
```
Core Framework:
  - fastapi: Web API framework
  - uvicorn: ASGI server

LLM Integration:
  - ollama: Ollama Python client
  - langchain: LLM orchestration (optional)

Data Processing:
  - yt-dlp: YouTube transcript extraction
  - pydantic: Data validation
  - requests: HTTP client

Storage:
  - chromadb: Vector database
  - python-dotenv: Environment variables
```

### External Services
```
Local (required):
  - Ollama: Local LLM server

External (on-demand):
  - YouTube: Transcript extraction only
  - No other API calls needed
```

---

## 🔐 Security & Privacy

### Local Processing
- All processing happens on your machine
- No data sent to external services
- No API keys required
- Models stored locally: `~/.ollama/models`

### Data Storage
- Analysis history: `backend/data/memory/history.json`
- Cached transcripts: `backend/data/transcripts/`
- Preferences: `backend/data/memory/preferences.json`
- All stored locally, under your control

### Backup & Cleanup
```bash
# Backup analysis
cp -r backend/data ~/backup_youtube

# Clear transcript cache (keep history)
rm -rf backend/data/transcripts/*

# Clear everything
rm -rf backend/data/*
```

---

## 🔧 Configuration Hierarchy

1. **Default values** (hardcoded in `config.py`)
2. **Environment variables** (from `.env`)
3. **Runtime modifications** (via API)

Edit `backend/.env` to customize:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Model Parameters
MAX_TOKENS=2000
TEMPERATURE=0.7
TOP_P=0.95

# Storage
MEMORY_PATH=./data/memory
TRANSCRIPT_CACHE=./data/transcripts

# API
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
DEBUG=False
```

---

## 📊 Processing Pipeline

### Full Analysis Flow

```python
# 1. User Input
url = "https://www.youtube.com/watch?v=..."

# 2. Orchestrator coordinates everything
orchestrator = VideoAnalysisOrchestrator()

# 3. Extract transcript
transcript_data = extractor.extract(url)
# Returns: {
#   "video_id": "...",
#   "title": "...",
#   "transcript": [TranscriptSegment, ...],
#   "duration": 1200
# }

# 4. Generate summary
summary = summarizer.summarize(transcript_text)
# Returns: Summary(
#   short_summary: "...",
#   bullet_points: [...],
#   key_takeaways: [...],
#   topics: [...]
# )

# 5. Generate insights
insights = insight_generator.generate_insights(
    transcript_text,
    summary.short_summary
)
# Returns: Insights(
#   patterns: [...],
#   implications: [...],
#   action_items: [...],
#   related_topics: [...],
#   questions: [...]
# )

# 6. Check facts
fact_checks = fact_checker.check_facts(
    all_claims,
    transcript_text,
    transcript_segments
)
# Returns: [FactCheckResult, ...]

# 7. Store in memory
memory.save_analysis(analysis_result)

# 8. Return to user
return analysis_result
```

---

## 🧪 Testing Strategy

### Unit Tests
```bash
python test.py
```

Tests verify:
1. Configuration loading
2. Ollama connection
3. Each agent initialization
4. Memory storage
5. Guardrails validation
6. Full orchestrator

### Manual Testing
1. Health check: `curl http://localhost:8000/health`
2. Analyze video: Web UI at http://localhost:8080
3. View API docs: http://localhost:8000/docs

### Integration Testing
- Analyze 5-10 videos
- Verify results quality
- Check confidence scores
- Test caching

---

## 📈 Scaling Considerations

### Current Limitations
- Single model at a time
- Sequential processing
- No database backend
- Local storage only

### Future Improvements
- Database backend (PostgreSQL)
- Batch processing
- Multiple models
- Distributed processing
- Mobile app
- Browser extension

---

## 🎓 Learning Resources

### Understanding LLMs
- How models work
- Prompt engineering
- Token limits
- Temperature & parameters

### Understanding Multi-Agent Systems
- Agent specialization
- Data passing between agents
- Orchestration patterns
- Error handling

### Understanding This Project
- Architecture in `SETUP_GUIDE.md`
- Code in `backend/src/`
- Comments in each file
- API docs at `/docs`

---

## 🔍 Debugging Tips

### Enable Debug Mode
Edit `backend/.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Check Logs
- Backend logs appear in terminal
- API errors show in browser console
- Ollama logs in ollama terminal

### Common Debug Commands
```bash
# Check API status
curl http://localhost:8000/config

# Check Ollama
curl http://localhost:11434/api/tags

# Check models
ollama list

# Check ports
lsof -i :8000
lsof -i :8080
lsof -i :11434
```

---

## 📚 Next Reading

1. **START_HERE.md** - Quick 3-minute guide
2. **QUICKSTART.md** - Step-by-step setup
3. **COMPLETE_GUIDE.md** - Comprehensive guide
4. **README.md** - Full API reference
5. **Source code** - Well-commented code files

---

## 🎯 Quick Start Summary

```bash
# 1. Install Ollama
brew install ollama

# 2. Start service
ollama serve

# 3. Download model (new terminal)
ollama pull mistral

# 4. Navigate to project
cd /Users/viyangchaudhari/Projects/youtube

# 5. Setup Python
cd backend && python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Run tests
cd .. && python test.py

# 7. Start services
./run.sh

# 8. Open browser
open http://localhost:8080
```

---

**You're all set! Happy analyzing! 🚀**

*For detailed setup: See START_HERE.md or QUICKSTART.md*
