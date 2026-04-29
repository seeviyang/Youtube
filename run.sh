#!/bin/bash

# YouTube Video Analysis Agent - Run all services

echo "🎬 YouTube Video Analysis Agent"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Check if Ollama is running
echo "Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running!"
    echo "Please start Ollama in a new terminal:"
    echo "  ollama serve"
    exit 1
fi
echo -e "${GREEN}✓ Ollama is running${NC}"
echo ""

# Start backend API
echo -e "${BLUE}Starting Backend API...${NC}"
cd "$PROJECT_ROOT/backend"
PYTHONPATH="$PROJECT_ROOT/backend:$PROJECT_ROOT/backend/src" \
  "$PROJECT_ROOT/backend/venv/bin/python" start.py > /dev/null 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
sleep 3

# Start frontend server
echo -e "${BLUE}Starting Frontend Server...${NC}"
cd "$PROJECT_ROOT/frontend"
python -m http.server 8080 > /dev/null 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""

# Display URLs
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo -e "${YELLOW}✨ Services are running!${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo ""
echo "📱 Frontend:  http://localhost:8080"
echo "🔌 API:       http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo; echo 'Services stopped'; exit" SIGINT

wait
