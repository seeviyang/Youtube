#!/bin/bash

# 🎬 YOUTUBE VIDEO ANALYSIS AGENT - STEP-BY-STEP SETUP
# Complete commands to run the system locally with Ollama

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   YouTube Video Analysis Agent - Step-by-Step Setup Guide    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# PHASE 1: VERIFY PREREQUISITES (5 minutes)
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 1: VERIFY PREREQUISITES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Step 1: Check Python version"
echo "  Command: python3 --version"
echo "  Expected: Python 3.9 or higher"
echo ""
python3 --version
echo ""

echo "Step 2: Check if Ollama is installed"
echo "  Command: ollama --version"
echo "  Expected: ollama version X.X.X"
echo ""
if command -v ollama &> /dev/null; then
    ollama --version
else
    echo "  ❌ Ollama not found. Please install from: https://ollama.ai"
    exit 1
fi
echo ""

echo "✅ Prerequisites verified!"
echo ""

# ============================================================================
# PHASE 2: SETUP OLLAMA SERVICE (10 minutes)
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 2: SETUP OLLAMA SERVICE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Step 3: Start Ollama service (OPEN NEW TERMINAL)"
echo "  ⚠️  IMPORTANT: Run this in a NEW terminal and keep it running"
echo ""
echo "  Command: ollama serve"
echo ""
echo "  Expected output:"
echo "    time=2024-01-15T10:30:00.123Z level=INFO msg=\"Listening on 127.0.0.1:11434\""
echo ""
echo "  📝 After running the above, continue in THIS terminal..."
echo ""

echo "Step 4: Download Ollama model (in ANOTHER NEW terminal)"
echo "  ⚠️  Wait for Ollama service to start first!"
echo ""
echo "  Command: ollama pull mistral"
echo ""
echo "  This will download ~4GB of data (5-10 minutes)"
echo "  Expected output: 'successfully pulled model'"
echo ""

echo "Step 5: Verify model is available"
echo "  Command: ollama list"
echo "  Expected output should show 'mistral' in the list"
echo ""

echo ""

# ============================================================================
# PHASE 3: SETUP PYTHON ENVIRONMENT (5 minutes)
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 3: SETUP PYTHON ENVIRONMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Step 6: Navigate to backend directory"
echo "  Command: cd /Users/viyangchaudhari/Projects/youtube/backend"
echo ""

echo "Step 7: Create Python virtual environment"
echo "  Command: python3 -m venv venv"
echo "  This creates a 'venv' folder (2-3 seconds)"
echo ""

echo "Step 8: Activate virtual environment"
echo "  Command (macOS/Linux): source venv/bin/activate"
echo "  Command (Windows): venv\\Scripts\\activate"
echo "  You should see '(venv)' at the start of your terminal prompt"
echo ""

echo "Step 9: Install Python dependencies"
echo "  Command: pip install -r requirements.txt"
echo "  This installs ~11 packages (2-5 minutes)"
echo ""
echo "  Packages installed:"
echo "    - fastapi (web framework)"
echo "    - ollama (LLM client)"
echo "    - yt-dlp (YouTube extraction)"
echo "    - pydantic (data validation)"
echo "    - chromadb (storage)"
echo "    - And 6 more..."
echo ""

echo ""

# ============================================================================
# PHASE 4: SYSTEM VERIFICATION (2 minutes)
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 4: SYSTEM VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Step 10: Navigate back to project root"
echo "  Command: cd /Users/viyangchaudhari/Projects/youtube"
echo ""

echo "Step 11: Run automated tests"
echo "  Command: python test.py"
echo "  Expected output:"
echo "    ✅ ALL TESTS PASSED (9/9)"
echo ""

echo "  If tests fail, check:"
echo "    1. Ollama service is running: ollama serve"
echo "    2. Model is available: ollama list"
echo "    3. All packages installed: pip install -r requirements.txt"
echo ""

echo ""

# ============================================================================
# PHASE 5: LAUNCH SERVICES (2 minutes)
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 5: LAUNCH SERVICES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "OPTION A: Start Everything at Once (RECOMMENDED)"
echo ""
echo "  Command: ./run.sh"
echo ""
echo "  This starts:"
echo "    1. Backend API on http://localhost:8000"
echo "    2. Frontend UI on http://localhost:8080"
echo ""
echo "  To stop: Press Ctrl+C"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "OPTION B: Manual Start (For Development)"
echo ""
echo "  Terminal 1 (Ollama - should be running):"
echo "    Command: ollama serve"
echo ""
echo "  Terminal 2 (Backend API):"
echo "    $ cd /Users/viyangchaudhari/Projects/youtube/backend"
echo "    $ source venv/bin/activate"
echo "    $ python src/main.py"
echo "    Expected output: 'Listening on http://0.0.0.0:8000'"
echo ""
echo "  Terminal 3 (Frontend):"
echo "    $ cd /Users/viyangchaudhari/Projects/youtube/frontend"
echo "    $ python -m http.server 8080"
echo "    Expected output: 'Serving HTTP on 0.0.0.0 port 8080'"
echo ""

echo ""

# ============================================================================
# PHASE 6: ACCESS THE SYSTEM
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 6: ACCESS THE SYSTEM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Step 12: Open the Web Interface"
echo "  URL: http://localhost:8080"
echo "  Expected: Beautiful UI with 'YouTube URL' input field"
echo ""

echo "Step 13: Open API Documentation (optional)"
echo "  URL: http://localhost:8000/docs"
echo "  Expected: Interactive Swagger API explorer"
echo ""

echo "Step 14: Check System Health"
echo "  Command: curl http://localhost:8000/health"
echo "  Expected output: {'status': 'healthy', 'ollama_connected': true}"
echo ""

echo ""

# ============================================================================
# PHASE 7: ANALYZE YOUR FIRST VIDEO
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 7: ANALYZE YOUR FIRST VIDEO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Step 15: Go to http://localhost:8080"
echo ""

echo "Step 16: Paste a YouTube URL"
echo "  Example videos with captions:"
echo "    - TED Talks"
echo "    - YouTube Learn videos"
echo "    - Tech conference talks"
echo "    - Educational videos"
echo ""

echo "Step 17: Click 'Analyze Video'"
echo "  Wait 2-3 minutes for analysis"
echo ""
echo "  The system will:"
echo "    1. Extract transcript (10-20 sec)"
echo "    2. Generate summary (30-60 sec)"
echo "    3. Create insights (30-60 sec)"
echo "    4. Check facts (10-30 sec)"
echo ""

echo "Step 18: View Results"
echo "  You should see:"
echo "    ✅ Short summary"
echo "    ✅ Key bullet points"
echo "    ✅ Deep insights"
echo "    ✅ Fact check results"
echo "    ✅ Confidence scores"
echo ""

echo ""

# ============================================================================
# COMPLETE COMMAND REFERENCE
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "QUICK COMMAND REFERENCE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📝 ONE-TIME SETUP (First run only):"
echo ""
echo "  # Terminal 1: Start Ollama (keep running)"
echo "  ollama serve"
echo ""
echo "  # Terminal 2: Download model"
echo "  ollama pull mistral"
echo ""
echo "  # Terminal 3: Setup Python"
echo "  cd /Users/viyangchaudhari/Projects/youtube/backend"
echo "  python3 -m venv venv"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo ""
echo "  # Run tests"
echo "  cd .."
echo "  python test.py"
echo ""

echo "🚀 LAUNCH (Every time you want to use it):"
echo ""
echo "  # Make sure Ollama is running"
echo "  ollama serve  # In Terminal 1"
echo ""
echo "  # Then run all services"
echo "  cd /Users/viyangchaudhari/Projects/youtube"
echo "  ./run.sh"
echo ""
echo "  # Open in browser"
echo "  open http://localhost:8080"
echo ""

echo "🔧 INDIVIDUAL SERVICE STARTUP (for development):"
echo ""
echo "  # Backend API (Terminal 2)"
echo "  cd backend && source venv/bin/activate && python src/main.py"
echo ""
echo "  # Frontend (Terminal 3)"
echo "  cd frontend && python -m http.server 8080"
echo ""

echo ""

# ============================================================================
# COMMON ISSUES & SOLUTIONS
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TROUBLESHOOTING"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "❌ Issue: 'Connection refused: localhost:11434'"
echo "   Solution: Start Ollama in Terminal 1"
echo "   Command: ollama serve"
echo ""

echo "❌ Issue: 'Model not found'"
echo "   Solution: Download mistral model"
echo "   Command: ollama pull mistral"
echo ""

echo "❌ Issue: 'ModuleNotFoundError: No module named fastapi'"
echo "   Solution: Install dependencies"
echo "   Command: pip install -r requirements.txt"
echo ""

echo "❌ Issue: 'Permission denied' running run.sh"
echo "   Solution: Make script executable"
echo "   Command: chmod +x run.sh"
echo ""

echo "❌ Issue: 'Address already in use' (port 8000 or 8080)"
echo "   Solution: Find and kill process on that port"
echo "   Commands:"
echo "     lsof -i :8000  (to find what's using port 8000)"
echo "     kill -9 <PID>  (to kill the process)"
echo ""

echo "❌ Issue: Analysis is very slow (> 5 minutes)"
echo "   Solution: Your system is slow or model is large"
echo "   Options:"
echo "     1. Use faster model: ollama pull neural-chat"
echo "     2. Close other applications"
echo "     3. Check system resources: top"
echo ""

echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ YOU'RE READY!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Your YouTube Video Analysis Agent is ready to use!"
echo ""
echo "Total time to setup: ~30-45 minutes (mostly downloading)"
echo "Time to first analysis: 2-3 minutes"
echo ""

echo "🎬 NEXT STEPS:"
echo ""
echo "  1. Read: START_HERE.md or INDEX.md"
echo "  2. Run: ./run.sh"
echo "  3. Open: http://localhost:8080"
echo "  4. Analyze: Paste a YouTube URL"
echo ""

echo "📚 DOCUMENTATION:"
echo "  - START_HERE.md        (3 min quick start)"
echo "  - QUICKSTART.md        (15 min setup)"
echo "  - COMPLETE_GUIDE.md    (30 min comprehensive)"
echo "  - INDEX.md             (master navigation)"
echo ""

echo "🌐 SERVICES:"
echo "  - Frontend: http://localhost:8080"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Happy analyzing! 🚀"
echo ""
