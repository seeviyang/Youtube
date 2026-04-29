#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   YouTube Video Analysis Agent - Quick Start Setup         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Step 1: Check if Ollama is installed
echo -e "${YELLOW}Step 1: Checking Ollama installation...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
else
    echo -e "${RED}✗ Ollama is not installed${NC}"
    echo "Please install Ollama from: https://ollama.ai"
    echo ""
    echo "macOS: brew install ollama"
    echo "Linux: curl https://ollama.ai/install.sh | sh"
    exit 1
fi

# Step 2: Check if Ollama service is running
echo ""
echo -e "${YELLOW}Step 2: Checking if Ollama service is running...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama service is running${NC}"
else
    echo -e "${RED}⚠ Ollama service is not running${NC}"
    echo "Please start Ollama in a new terminal:"
    echo -e "${BLUE}  ollama serve${NC}"
    echo ""
    read -p "Press enter when Ollama is running..."
fi

# Step 3: Check for available models
echo ""
echo -e "${YELLOW}Step 3: Checking available models...${NC}"
MODELS=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | head -3)
if [ -z "$MODELS" ]; then
    echo -e "${YELLOW}⚠ No models found. Pulling 'mistral' model...${NC}"
    echo "This may take a few minutes..."
    ollama pull mistral
    echo -e "${GREEN}✓ Model downloaded${NC}"
else
    echo -e "${GREEN}✓ Available models:${NC}"
    echo "$MODELS"
fi

# Step 4: Check Python
echo ""
echo -e "${YELLOW}Step 4: Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python is installed: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

# Step 5: Install dependencies
echo ""
echo -e "${YELLOW}Step 5: Installing Python dependencies...${NC}"
cd "$(dirname "$0")/backend"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# Step 6: Create data directories
echo ""
echo -e "${YELLOW}Step 6: Creating data directories...${NC}"
mkdir -p data/memory data/transcripts
echo -e "${GREEN}✓ Data directories created${NC}"

# Step 7: Summary
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Setup complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Ollama (if not already running):"
echo -e "${BLUE}   ollama serve${NC}"
echo ""
echo "2. In a new terminal, start the backend API:"
echo -e "${BLUE}   cd backend && python src/main.py${NC}"
echo ""
echo "3. In another terminal, serve the frontend:"
echo -e "${BLUE}   cd frontend && python -m http.server 8080${NC}"
echo ""
echo "4. Open your browser:"
echo -e "${BLUE}   http://localhost:8080${NC}"
echo ""
echo "📚 API Documentation:"
echo -e "${BLUE}   http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Happy analyzing! 🎬${NC}"
