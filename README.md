# YouTube Video Analysis Agent System

A sophisticated multi-agent system that analyzes YouTube videos and generates concise summaries, key insights, and timestamps using local LLM inference with Ollama.

## 🎯 Key Features

✅ **Multi-Agent Architecture**
- Transcript Extraction Agent
- Content Summarizer Agent
- Insight Generator Agent
- Fact Checker Agent

✅ **Structured Outputs**
- Short summaries (2-3 sentences)
- Bullet-point key takeaways (5-7 points)
- Deeper insights and patterns
- Timestamp-based topic segmentation
- Confidence scoring

✅ **Memory & Personalization**
- Analysis history storage
- Similar video recommendations
- User preference tracking
- Session-based context

✅ **Guardrails & Safety**
- Hallucination detection
- Fact-checking against transcripts
- Confidence-based filtering
- Output validation

✅ **Local Processing**
- Ollama integration for local LLM inference
- No API keys required
- Privacy-first approach
- Offline capability

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Ollama installed
- 8GB+ RAM (16GB recommended)

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### 2. Start Ollama Service

```bash
ollama serve
```

### 3. Pull a Model

In a new terminal:
```bash
ollama pull mistral
```

### 4. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Configure Environment

Create/verify `.env` file:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
MEMORY_PATH=./data/memory
TRANSCRIPT_CACHE=./data/transcripts
```

### 6. Run the API Server

```bash
python src/main.py
```

Server starts at: `http://localhost:8000`

### 7. Analyze a Video

Open `http://localhost:8000/docs` and use the `/analyze` endpoint:

```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "use_cache": true
}
```

Or use curl:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=..."}'
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check (requires Ollama) |
| POST | `/analyze` | Analyze a YouTube video |
| GET | `/history` | Get previous analyses |
| GET | `/similar/{video_id}` | Find similar videos |
| GET | `/config` | Get current configuration |

## 🏗️ Project Structure

```
youtube/
├── backend/
│   ├── src/
│   │   ├── agents/
│   │   │   ├── transcript_extractor.py   # Extract YouTube transcripts
│   │   │   ├── summarizer.py             # Generate summaries
│   │   │   ├── insight_generator.py      # Extract insights
│   │   │   └── fact_checker.py           # Validate facts
│   │   ├── memory/
│   │   │   └── storage.py                # Store analysis history
│   │   ├── config.py                     # Configuration management
│   │   ├── guardrails.py                 # Safety & validation
│   │   ├── orchestrator.py               # Coordinate all agents
│   │   └── main.py                       # FastAPI server
│   ├── requirements.txt
│   ├── .env
│   └── package.json
├── frontend/                              # (Optional UI)
└── README.md
```

## 🤖 How It Works

### Analysis Pipeline

```
YouTube URL
    ↓
[Transcript Extraction]
    ↓
[Content Summarization]
    ├─→ Short summary
    ├─→ Bullet points
    ├─→ Key takeaways
    └─→ Topics
    ↓
[Insight Generation]
    ├─→ Patterns
    ├─→ Implications
    ├─→ Action items
    └─→ Follow-up questions
    ↓
[Fact Checking]
    ├─→ Verify claims
    ├─→ Confidence scoring
    └─→ Evidence citations
    ↓
[Memory Storage]
    └─→ Save analysis
```

## 🛡️ Guardrails & Safety

### Hallucination Prevention
- Detects uncertainty patterns
- Validates facts against transcript
- Flags unsupported claims
- Confidence scoring

### Output Validation
- Length checks (min/max)
- Format validation
- Incompleteness detection
- Topic coherence

### Content Filtering
- Inappropriate content detection
- Bias awareness
- Harmful content flags

## 📊 Output Example

```json
{
  "metadata": {
    "video_id": "...",
    "title": "Video Title",
    "duration_seconds": 1200,
    "transcript_segments_count": 150
  },
  "summary": {
    "short_summary": "...",
    "bullet_points": ["...", "...", "..."],
    "key_takeaways": ["...", "...", "..."],
    "topics": ["Topic 1", "Topic 2", "..."]
  },
  "insights": {
    "patterns": ["Pattern 1", "Pattern 2", "..."],
    "implications": ["Implication 1", "..."],
    "action_items": ["Action 1", "Action 2", "..."],
    "questions": ["Question 1", "..."]
  },
  "fact_check": {
    "summary": {
      "support_percentage": 85.5,
      "average_confidence": 0.82
    },
    "detailed_results": [...]
  },
  "quality_metrics": {
    "overall_confidence": 0.85
  }
}
```

## ⚙️ Configuration

Edit `backend/.env` to customize:

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral              # mistral, neural-chat, llama2, etc.

# Model parameters
MAX_TOKENS=2000                   # Reduce for faster responses
TEMPERATURE=0.7                   # 0=deterministic, 1=creative

# Memory
MEMORY_TYPE=chromadb
MEMORY_PATH=./data/memory

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 🔧 Model Selection

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| mistral | 4GB | Fast | Good | General use, balance |
| neural-chat | 4GB | Fast | Good | Chat tasks |
| llama2 | 7GB | Medium | Excellent | Accuracy-critical |
| dolphin-mixtral | 26GB | Slow | Excellent | Complex analysis |

Start with **mistral** for fastest development.

## 📝 Example Usage

### Python Script

```python
from src.orchestrator import VideoAnalysisOrchestrator

orchestrator = VideoAnalysisOrchestrator()

# Analyze video
result = orchestrator.analyze("https://www.youtube.com/watch?v=...")

# Access results
print(f"Summary: {result['summary']['short_summary']}")
print(f"Confidence: {result['quality_metrics']['overall_confidence']}")

# Get previous analyses
history = orchestrator.get_previous_analyses(limit=5)

# Find similar videos
similar = orchestrator.find_similar_videos(result['metadata']['video_id'])
```

### API Usage

```bash
# Health check
curl http://localhost:8000/health

# Analyze video
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=..."}'

# Get history
curl http://localhost:8000/history?limit=5

# View API documentation
open http://localhost:8000/docs
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Connection refused localhost:11434` | Make sure `ollama serve` is running |
| `Model not found` | Run `ollama pull mistral` |
| `Slow responses` | Use smaller model or increase timeout in .env |
| `Memory errors` | Reduce MAX_TOKENS or use smaller model |
| `No transcript available` | Video may have disabled captions |

## 📚 Next Steps

- [ ] Build frontend UI (React/Vue/Angular)
- [ ] Add streaming responses for long-running analyses
- [ ] Implement ChromaDB vector storage
- [ ] Add batch video processing
- [ ] Create comparison views for multiple videos
- [ ] Add export functionality (PDF/Markdown)
- [ ] Implement advanced filtering and search
- [ ] Add user authentication
- [ ] Deploy to cloud

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Better transcript quality handling
- More sophisticated fact-checking
- Enhanced insight generation
- Frontend development
- Additional guardrails

## 📄 License

MIT License - feel free to use and modify

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM inference
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube transcript extraction
- [LangChain](https://python.langchain.com) - LLM orchestration
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Check Ollama logs for connection issues

---

**Ready to analyze videos?** Start with:
```bash
ollama serve
```

Then in another terminal:
```bash
cd backend && python src/main.py
```

Visit: http://localhost:8000/docs 🚀
