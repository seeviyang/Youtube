#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "\n${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $1${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if Docker is installed
print_header "Checking Prerequisites"

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    echo "Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi
print_success "Docker is installed"

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed"
    exit 1
fi
print_success "Docker Compose is installed"

# Display current directory
print_info "Working directory: $(pwd)"

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found"
    exit 1
fi
print_success "docker-compose.yml found"

# Menu
print_header "YouTube Analyzer - Docker Deployment"

echo "Select an option:"
echo ""
echo "  1. Start all services (development)"
echo "  2. Start with logs visible"
echo "  3. Stop all services"
echo "  4. View logs"
echo "  5. Rebuild images"
echo "  6. Pull Ollama model"
echo "  7. Health check"
echo "  8. Clean up everything"
echo "  9. Exit"
echo ""
read -p "Enter your choice [1-9]: " choice

case $choice in
    1)
        print_header "Starting Services (Background)"
        docker-compose up -d
        
        if [ $? -eq 0 ]; then
            print_success "Services started successfully"
            echo ""
            echo "Access your application:"
            echo "  Frontend:  http://localhost:3000"
            echo "  Backend:   http://localhost:8000"
            echo "  API Docs:  http://localhost:8000/docs"
            echo ""
            echo "Check status with: docker-compose ps"
            echo "View logs with: docker-compose logs -f"
        else
            print_error "Failed to start services"
            exit 1
        fi
        ;;
    
    2)
        print_header "Starting Services (With Logs)"
        echo "Press Ctrl+C to stop"
        sleep 2
        docker-compose up
        ;;
    
    3)
        print_header "Stopping Services"
        docker-compose stop
        print_success "Services stopped"
        ;;
    
    4)
        print_header "Service Logs"
        echo ""
        echo "Select service:"
        echo "  1. All"
        echo "  2. Backend"
        echo "  3. Frontend"
        echo "  4. Ollama"
        echo ""
        read -p "Enter choice [1-4]: " log_choice
        
        case $log_choice in
            1) docker-compose logs -f ;;
            2) docker-compose logs -f backend ;;
            3) docker-compose logs -f frontend ;;
            4) docker-compose logs -f ollama ;;
            *) print_error "Invalid choice" ;;
        esac
        ;;
    
    5)
        print_header "Rebuilding Images"
        print_info "This may take a few minutes..."
        docker-compose build --no-cache
        if [ $? -eq 0 ]; then
            print_success "Images rebuilt successfully"
        else
            print_error "Build failed"
            exit 1
        fi
        ;;
    
    6)
        print_header "Pulling Ollama Model"
        print_info "This may take 5-10 minutes on first run..."
        
        # First ensure Ollama container is running
        docker-compose up -d ollama
        sleep 5
        
        docker-compose exec ollama ollama pull mistral
        if [ $? -eq 0 ]; then
            print_success "Ollama model pulled successfully"
        else
            print_error "Failed to pull model"
            exit 1
        fi
        ;;
    
    7)
        print_header "Health Check"
        
        echo "Checking services..."
        echo ""
        
        # Check backend
        echo -n "Backend: "
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_success "Running"
        else
            print_error "Not responding"
        fi
        
        # Check frontend
        echo -n "Frontend: "
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Running"
        else
            print_error "Not responding"
        fi
        
        # Check Ollama
        echo -n "Ollama: "
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            print_success "Running"
        else
            print_error "Not responding"
        fi
        
        echo ""
        docker-compose ps
        ;;
    
    8)
        print_header "Clean Up"
        echo ""
        read -p "Are you sure? This will remove all containers and volumes (y/n): " confirm
        
        if [ "$confirm" = "y" ]; then
            docker-compose down -v
            docker system prune -f
            print_success "Cleanup completed"
        else
            print_info "Cleanup cancelled"
        fi
        ;;
    
    9)
        print_info "Exiting..."
        exit 0
        ;;
    
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
