#!/bin/bash

# Docker Daemon Quick Fix Script for macOS

echo ""
echo "🐳 Docker Daemon Quick Fix"
echo "=========================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo ""
    echo "Download from: https://www.docker.com/products/docker-desktop"
    echo ""
    exit 1
fi

echo "✅ Docker is installed: $(docker --version)"
echo ""

# Check if Docker daemon is running
echo "Checking if Docker daemon is running..."
if docker ps &> /dev/null; then
    echo "✅ Docker daemon is running!"
    echo ""
    echo "You can now run: ./deploy.sh"
    exit 0
else
    echo "❌ Docker daemon is NOT running"
    echo ""
    echo "Starting Docker Desktop..."
    echo ""
    
    # Try to start Docker
    if [ -f "/Applications/Docker.app/Contents/MacOS/Docker" ]; then
        open -a Docker
        echo "Docker is starting..."
        echo ""
        echo "This may take 30-60 seconds..."
        echo ""
        
        # Wait and retry
        for i in {1..60}; do
            echo -n "."
            if docker ps &> /dev/null; then
                echo ""
                echo ""
                echo "✅ Docker daemon started successfully!"
                echo ""
                echo "You can now run: ./deploy.sh"
                exit 0
            fi
            sleep 1
        done
        
        echo ""
        echo "❌ Docker didn't start in time"
        echo ""
        echo "Troubleshooting:"
        echo "1. Check that Docker.app opened"
        echo "2. Check menu bar for Docker icon"
        echo "3. Wait a bit longer and try again"
        echo "4. Read DOCKER_DAEMON_FIX.md for more help"
        exit 1
    else
        echo "❌ Docker.app not found in /Applications"
        echo ""
        echo "Please:"
        echo "1. Download from: https://www.docker.com/products/docker-desktop"
        echo "2. Install Docker"
        echo "3. Run this script again"
        exit 1
    fi
fi
