# YouTube Video Analysis Agent System - Local Setup Guide

A multi-agent system that analyzes YouTube videos, generates summaries, extracts insights, and validates facts using Ollama for local LLM inference.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    YouTube URL Input                         │
└────────────────────────────┬────────────────────────────────┘
                             │
┌─────────────────────────────▼────────────────────────────────┐
│         Transcript Extraction Agent (yt-dlp)                 │
│  Extracts transcript with timestamps from YouTube            │
└────────────────────────────┬────────────────────────────────┘
                             │
┌─────────────────────────────▼────────────────────────────────┐
│     Content Summarizer Agent (Ollama + LLM)                  │
│  Generates bullet points, short summary, key takeaways      │
└────────────────────────────┬────────────────────────────────┘
                             │
┌─────────────────────────────▼────────────────────────────────┐
│      Insight Generator Agent (Ollama + LLM)                  │
│  Extracts deeper insights, patterns, actionable tips        │
└────────────────────────────┬────────────────────────────────┘
                             │
┌─────────────────────────────▼────────────────────────────────┐
│      Fact Checker Agent (Validation + Confidence)            │
│  Validates claims, flags hallucinations, confidence scoring  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌─────────────────────────────▼────────────────────────────────┐
│              Memory System (ChromaDB/Local)                   │
│  Stores: Previous analyses, user preferences, history        │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Python 3.9+**
- **Ollama** installed and running
- **macOS/Linux/Windows** with 8GB+ RAM (16GB recommended for better performance)
- **pip** or **conda** for Python package management

## Step-by-Step Setup

### Step 1: Install Ollama

**macOS:**
```bash
# Download from ollama.ai
# Or use Homebrew
brew install ollama
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai)

### Step 2: Pull Required Models

Start Ollama service:
```bash
ollama serve
```

In a new terminal, pull models:
```bash
# Main model for summarization and insight generation
ollama pull mistral  # Fast, good quality (4.1B params)
# OR
ollama pull neural-chat  # Alternative, optimized for chat
# OR
ollama pull dolphin-mixtral  # More capable but larger

# Optional: For fact-checking
ollama pull llama2  # Slower but more accurate
```

For local testing, start with `mistral` (faster, ~4GB).

### Step 3: Create Project Structure

```
youtube/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── transcript_extractor.py
│   │   │   ├── summarizer.py
│   │   │   ├── insight_generator.py
│   │   │   └── fact_checker.py
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   └── storage.py
│   │   ├── orchestrator.py
│   │   ├── guardrails.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
└── README.md
```

### Step 4: Install Python Dependencies

Create `requirements.txt`:
```
python-dotenv==1.0.0
requests==2.31.0
langchain==0.1.0
langchain-community==0.1.0
ollama==0.0.50
yt-dlp==2024.1.1
pydantic==2.5.0
chromadb==0.4.17
fastapi==0.109.0
uvicorn==0.27.0
httpx==0.25.0
```

Install:
```bash
cd backend
pip install -r requirements.txt
```

### Step 5: Configure Environment

Create `backend/.env`:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
MEMORY_TYPE=chromadb
MEMORY_PATH=./data/memory
TRANSCRIPT_CACHE=./data/transcripts
```

### Step 6: Verify Ollama Connection

Test connection:
```bash
curl http://localhost:11434/api/tags
```

Should return list of available models.

## Key Components

### 1. Transcript Extractor
- Uses `yt-dlp` to fetch YouTube transcripts
- Returns structured data with timestamps
- Handles captions, auto-generated, and manual transcripts

### 2. Content Summarizer
- Generates 2-3 paragraph summary
- Creates 5-7 key bullet points
- Identifies main topics
- Uses structured prompting

### 3. Insight Generator
- Extracts actionable insights
- Identifies patterns and implications
- Generates related questions
- Provides learning paths

### 4. Fact Checker
- Validates claims in summaries
- Flags potential hallucinations
- Confidence scoring
- Sources references to transcript timestamps

### 5. Memory System
- ChromaDB for vector storage
- Session-based user preferences
- Analysis history
- Similar video recommendations

### 6. Guardrails
- Hallucination detection
- Confidence thresholds
- Output validation
- Content filters

## Running the System

### Terminal 1: Start Ollama
```bash
ollama serve
```

### Terminal 2: Run Backend
```bash
cd backend
python src/main.py
```

### Terminal 3: Serve Frontend
```bash
python -m http.server 8080 --directory ./frontend
```

Then open: `http://localhost:8080`

## Testing

### Quick Test Script
```bash
python backend/src/test.py
```

### Example Usage
```python
from src.orchestrator import VideoAnalysisOrchestrator

orchestrator = VideoAnalysisOrchestrator()
result = orchestrator.analyze("https://www.youtube.com/watch?v=...")
print(result)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Connection refused: localhost:11434` | Make sure `ollama serve` is running |
| `Model not found` | Run `ollama pull mistral` |
| `Slow responses` | Use smaller model or increase timeout |
| `Memory issues` | Reduce model size or increase system RAM |

## Performance Tips

1. **Model Selection**: mistral (fast), neural-chat (balanced), llama2 (accurate)
2. **Memory**: Use smaller chunks for transcripts (500-1000 tokens)
3. **Caching**: Enable transcript caching to avoid re-fetching
4. **Batch Processing**: Process multiple videos sequentially for stability
5. **Timeout**: Set request timeout to 60-120 seconds

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull models
3. ✅ Set up project structure
4. ✅ Install dependencies
5. ✅ Configure environment
6. ✅ Test connection
7. Build agents
8. Implement orchestrator
9. Add memory system
10. Create frontend UI

## References

- [Ollama Documentation](https://ollama.ai)
- [LangChain Documentation](https://python.langchain.com)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [ChromaDB Documentation](https://docs.trychroma.com)
