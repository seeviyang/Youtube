# 🐳 Docker Deployment Guide for YouTube Project

Complete guide to deploy the YouTube Video Analysis Agent using Docker and Nginx for network-wide access.

---

## 📋 Prerequisites

- **Docker** installed ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** installed ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **8GB+ RAM** recommended
- **Ports available**: 80 (HTTP), 443 (HTTPS), 11434 (Ollama)

---

## 🚀 Quick Start (Production Deployment)

### 1. Start All Services with Nginx

```bash
cd /Users/viyangchaudhari/Projects/youtube

# Start with production profile (includes Nginx)
docker-compose --profile production up -d
```

This will start:
- ✅ **Ollama** (LLM service) on port 11434
- ✅ **Backend API** (FastAPI) on port 8000 (internal)
- ✅ **Frontend** (Web UI) on port 3000 (internal)
- ✅ **Nginx** (Reverse Proxy) on ports 80 & 443

### 2. Access the Application

**From any machine on the network:**
- **Main URL**: `http://<YOUR_MACHINE_IP>:80`
- **API Direct**: `http://<YOUR_MACHINE_IP>:8000`
- **Ollama Direct**: `http://<YOUR_MACHINE_IP>:11434`

**Find your machine IP:**

```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

---

## 🔧 Detailed Setup Instructions

### Step 1: Verify Docker Installation

```bash
docker --version
docker-compose --version
```

### Step 2: Build Images (First Time Only)

```bash
cd /Users/viyangchaudhari/Projects/youtube

# Build all images
docker-compose build

# Or build with production profile
docker-compose --profile production build
```

### Step 3: Configure Environment

The project uses default environment variables. To customize:

```bash
# Backend configuration
cat backend/.env
# Edit if needed:
# OLLAMA_URL=http://ollama:11434
# OLLAMA_MODEL=mistral
```

### Step 4: Start Services

**Option A: Development Mode (without Nginx)**
```bash
docker-compose up -d
```

**Option B: Production Mode (with Nginx & SSL-ready)**
```bash
docker-compose --profile production up -d
```

### Step 5: Verify All Containers Are Running

```bash
docker-compose ps
```

Expected output:
```
CONTAINER ID   IMAGE                 STATUS              PORTS
xxx            ollama/ollama         Up (healthy)        11434->11434/tcp
xxx            youtube-backend       Up (healthy)        8000->8000/tcp
xxx            youtube-frontend      Up (healthy)        3000->3000/tcp
xxx            nginx:alpine          Up                  80->80/tcp, 443->443/tcp
```

### Step 6: Test Services

```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check Backend API
curl http://localhost:8000/health

# Check Frontend (through Nginx)
curl http://localhost

# View Nginx logs
docker-compose logs nginx
```

---

## 🌐 Accessing from Other Machines

### Method 1: Using Machine IP (HTTP)

```bash
# Find your machine IP
ifconfig | grep "inet "

# Access from another machine
# Open browser: http://<YOUR_IP>
# Example: http://192.168.1.100
```

### Method 2: Using Hostname (if mDNS enabled)

```bash
# On some networks, use:
http://<HOSTNAME>.local
# Example: http://MacBook-Pro.local
```

### Method 3: Using Fixed IP or DNS

- Set static IP on your machine
- Configure DNS A record to point to your IP
- Access via domain name

---

## 🔐 HTTPS/SSL Configuration

### Enable HTTPS with Self-Signed Certificate

```bash
# Create SSL directory
mkdir -p /Users/viyangchaudhari/Projects/youtube/ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /Users/viyangchaudhari/Projects/youtube/ssl/key.pem \
  -out /Users/viyangchaudhari/Projects/youtube/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Org/CN=localhost"

# Update nginx.conf to enable HTTPS (uncomment HTTPS section)
# Then restart Nginx
docker-compose --profile production restart nginx
```

### Update Nginx Configuration for HTTPS

In `nginx.conf`, uncomment and update the HTTPS section:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;  # Change this to your domain
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # ... rest of configuration
}
```

---

## 📊 Container Management

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f nginx
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ollama

# Last 50 lines
docker-compose logs --tail=50 nginx
```

### Stop Services

```bash
# Stop all
docker-compose stop

# Stop with production profile
docker-compose --profile production stop
```

### Remove Containers & Data

```bash
# Stop and remove containers (keeps data)
docker-compose down

# Remove containers and volumes (WARNING: deletes data)
docker-compose down -v
```

### Restart Services

```bash
docker-compose restart

# Restart specific service
docker-compose restart backend
```

---

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check if ports are in use
lsof -i :80
lsof -i :8000
lsof -i :3000

# Stop all Docker containers
docker stop $(docker ps -q)

# Try starting again
docker-compose up -d
```

### Nginx Can't Connect to Backend

```bash
# Verify backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Verify network connectivity
docker-compose exec nginx ping backend
docker-compose exec nginx curl http://backend:8000/health
```

### Ollama Not Available

```bash
# Check Ollama container
docker-compose logs ollama

# Verify model is loaded
docker-compose exec ollama ollama list

# Pull a model if needed
docker-compose exec ollama ollama pull mistral
```

### Can't Access from Other Machines

```bash
# Check your machine's firewall
# macOS: System Preferences > Security & Privacy > Firewall

# Check if Nginx is listening on all interfaces
docker-compose exec nginx netstat -tulpn | grep 80

# Test from another machine
curl http://<YOUR_IP>:80
curl http://<YOUR_IP>:8000

# Check frontend environment variables
docker-compose exec frontend env | grep API_URL
```

---

## 📈 Scaling & Performance

### Increase Resources

Edit `docker-compose.yml` to add resource limits:

```yaml
services:
  backend:
    # ... existing config
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Enable Ollama GPU Support

Edit `docker-compose.yml`:

```yaml
services:
  ollama:
    # ... existing config
    runtime: nvidia  # For NVIDIA GPU
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

---

## 🔄 Update & Maintenance

### Rebuild Images After Code Changes

```bash
docker-compose down
docker-compose build --no-cache
docker-compose --profile production up -d
```

### Clean Up Unused Docker Resources

```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

---

## 📝 Environment Variables Reference

### Backend (.env)
```
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral
API_HOST=0.0.0.0
API_PORT=8000
PYTHONUNBUFFERED=1
```

### Frontend
```
REACT_APP_API_URL=http://localhost:8000
NODE_ENV=production
```

### Ollama
```
OLLAMA_HOST=0.0.0.0:11434
```

---

## 🎯 Network Architecture

```
┌─────────────────────────────────────────────┐
│         External Network / Internet          │
│    (Other machines accessing port 80/443)    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   Nginx (Port 80)   │
         │   (Reverse Proxy)   │
         └──┬──────────────┬───┘
            │              │
     ┌──────▼────────┐  ┌──▼────────────────┐
     │  Frontend     │  │  Backend API     │
     │  (Port 3000)  │  │  (Port 8000)     │
     └──────┬────────┘  └────────┬─────────┘
            │                    │
            └────────────┬───────┘
                         │
                    ┌────▼────────┐
                    │ Ollama LLM   │
                    │ (Port 11434) │
                    └─────────────┘
```

---

## ✅ Deployment Checklist

- [ ] Docker & Docker Compose installed
- [ ] All ports (80, 443, 8000, 3000, 11434) available
- [ ] Project files at `/Users/viyangchaudhari/Projects/youtube`
- [ ] `docker-compose build` completed successfully
- [ ] `docker-compose --profile production up -d` started
- [ ] All containers running: `docker-compose ps`
- [ ] Verified access from local machine: `http://localhost`
- [ ] Verified access from other machine: `http://<YOUR_IP>`
- [ ] Backend API responding: `http://<YOUR_IP>:8000/health`
- [ ] Ollama responding: `http://<YOUR_IP>:11434/api/tags`

---

## 🆘 Support

For more information:
- Backend logs: `docker-compose logs -f backend`
- Frontend logs: `docker-compose logs -f frontend`
- Nginx logs: `docker-compose logs -f nginx`
- Check main README: [README.md](README.md)

