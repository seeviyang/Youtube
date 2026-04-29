# 🚀 YouTube Video Analysis Agent - Running Guide

## ✅ All Systems Go!

The project is now fully set up and running. Here's what's currently active:

### Services Running
- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:8080
- **API Documentation**: http://localhost:8000/docs
- **Ollama LLM**: http://localhost:11434 (with `mistral` model)

### Quick Commands

#### Start All Services
```bash
cd /Users/viyangchaudhari/Projects/youtube
./run.sh
```

#### Start Individual Services

**Backend only** (if Ollama already running):
```bash
cd /Users/viyangchaudhari/Projects/youtube/backend
PYTHONPATH="$(pwd):$(pwd)/src" ./venv/bin/python start.py
```

**Frontend only**:
```bash
cd /Users/viyangchaudhari/Projects/youtube/frontend
python3 -m http.server 8080
```

**Ollama** (if not running):
```bash
ollama serve
```

#### Stop All Services
```bash
killall -9 python python3 ollama 2>/dev/null
# or press Ctrl+C if running in foreground
```

### API Endpoints

- `GET /` - Root (shows API info)
- `GET /health` - Health check (includes Ollama status)
- `POST /analyze` - Analyze a YouTube video
- `GET /history` - Get previous analyses
- `GET /similar/{video_id}` - Find similar videos
- `GET /config` - Get current configuration
- `GET /docs` - Interactive API documentation (Swagger UI)

### Environment Variables

Backend config is in `backend/.env`:
- `OLLAMA_BASE_URL` - Ollama API URL (default: http://localhost:11434)
- `OLLAMA_MODEL` - Model to use (default: mistral)
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)

### Troubleshooting

**Port already in use**:
```bash
lsof -i :8000  # Check what's using port 8000
kill -9 <PID>  # Kill the process
```

**Ollama not connected**:
```bash
# Ensure Ollama is running:
ollama serve

# In another terminal, verify model:
ollama pull mistral
ollama list
```

**Module import errors**:
- Dependencies are in `backend/venv/`
- If getting import errors, ensure venv is activated or use full paths like in run.sh

### Test the System

```bash
# Test backend health
curl http://localhost:8000/health

# Test frontend loads
curl http://localhost:8080/ | head -5

# Test API docs available
curl http://localhost:8000/docs
```

### Next Steps

1. **Open UI**: Visit http://localhost:8080 in your browser
2. **Try API**: Go to http://localhost:8000/docs for interactive API docs
3. **Submit a video**: Use the frontend form to analyze a YouTube video
4. **Check results**: Results will appear in the frontend and can be retrieved via `/history`

---

**All services are currently running!** ✨
