# 🚀 Docker Deployment Guide - YouTube Video Analyzer

Complete guide to deploy backend and frontend on Docker and access them online.

---

## Table of Contents

1. [Quick Start (Local)](#quick-start-local)
2. [Docker Setup](#docker-setup)
3. [Online Deployment Options](#online-deployment-options)
4. [Production Deployment](#production-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Quick Start (Local)

### Prerequisites

- ✅ Docker installed (https://www.docker.com/products/docker-desktop)
- ✅ Docker Compose installed (comes with Docker Desktop)
- ✅ ~8GB free disk space for Ollama model
- ✅ Port 8000, 3000, 11434 available

### Step 1: Start Docker Containers

```bash
cd /Users/viyangchaudhari/Projects/youtube

# Start all services
docker-compose up -d

# Or with logs visible
docker-compose up
```

### Step 2: Wait for Ollama Model to Load

```bash
# Check Ollama container
docker-compose logs ollama

# Or manually pull the model
docker-compose exec ollama ollama pull mistral
```

### Step 3: Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Step 4: Test the System

```bash
# Health check backend
curl http://localhost:8000/health

# View logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs ollama

# Stop containers
docker-compose down
```

---

## Docker Setup

### File Structure

```
youtube/
├── backend/
│   ├── Dockerfile          (created)
│   ├── requirements.txt
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   └── agents/
│   └── data/              (volume mounted)
├── frontend/
│   ├── Dockerfile         (created)
│   ├── package.json
│   ├── index.html
│   └── app.js
├── docker-compose.yml     (created)
└── nginx.conf            (created)
```

### Understanding the Services

#### 1. **Ollama Service**
- Image: `ollama/ollama:latest`
- Port: 11434
- Purpose: LLM inference engine (mistral model)
- Volume: `ollama_data` (persistent model storage)

#### 2. **Backend Service**
- Dockerfile: Custom Python image
- Port: 8000
- Technology: FastAPI + Uvicorn
- Depends on: Ollama
- Features: Health checks, volume mounting, environment variables

#### 3. **Frontend Service**
- Dockerfile: Node.js + serve
- Port: 3000
- Technology: Static files served by Node
- Depends on: Backend API
- Features: Health checks, build artifacts

#### 4. **Nginx Service** (Optional - Production)
- Image: nginx:alpine
- Port: 80, 443
- Purpose: Reverse proxy, load balancing, SSL/TLS
- Profile: production (use `docker-compose --profile production up`)

### Docker Commands Reference

```bash
# Start all services
docker-compose up -d

# Start with specific service
docker-compose up -d backend

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute command in container
docker-compose exec backend bash
docker-compose exec ollama ollama list

# Stop all services
docker-compose down

# Remove volumes (data deletion)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# View running containers
docker-compose ps

# Stats
docker stats
```

---

## Online Deployment Options

### Option 1: **Railway** ⭐ (Recommended - Easiest)

**Benefits**: Free tier, automatic HTTPS, GitHub integration, easy to use

**Steps:**

1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project → Import from GitHub
4. Select your `youtube` repository
5. Railway auto-detects `docker-compose.yml`
6. Configure environment variables:
   ```
   OLLAMA_URL=http://ollama:11434
   REACT_APP_API_URL=https://your-domain.railway.app
   ```
7. Deploy!

**Result**: https://your-project.railway.app (public URL)

---

### Option 2: **Render** 

**Benefits**: Free tier, easy deployment, good documentation

**Steps:**

1. Go to https://render.com
2. Sign up with GitHub
3. Create new **Web Service**
4. Connect your GitHub repository
5. For each service, create separate Web Service:
   - Backend: `docker-compose run backend`
   - Frontend: `docker-compose run frontend`
6. Set environment variables
7. Deploy!

---

### Option 3: **AWS ECS** (Most Scalable)

**Benefits**: Highly scalable, auto-scaling, production-grade

**Steps:**

1. Create AWS account
2. Set up ECS cluster
3. Create task definitions from `docker-compose.yml`
4. Use AWS Fargate for serverless containers
5. Set up Application Load Balancer (ALB)
6. Connect domain via Route 53

**Cost**: ~$10-50/month (depends on usage)

---

### Option 4: **DigitalOcean App Platform**

**Benefits**: Simple, affordable, good for small projects

**Steps:**

1. Go to https://www.digitalocean.com
2. Create account
3. App Platform → Create App
4. Connect GitHub repository
5. Configure services
6. Deploy!

**Cost**: ~$5-20/month

---

### Option 5: **Self-Hosted (VPS)**

**Benefits**: Full control, potentially cheaper for long-term

**Steps:**

1. Get VPS:
   - DigitalOcean: $5/month
   - Linode: $5/month
   - AWS EC2: ~$7-15/month
   - Hetzner: ~$3/month

2. SSH into server
3. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

4. Clone repository:
   ```bash
   git clone https://github.com/seeviyang/youtube.git
   cd youtube
   ```

5. Start containers:
   ```bash
   docker-compose up -d
   ```

6. Set up domain with DNS
7. Configure SSL/TLS (Let's Encrypt)

---

## Production Deployment

### Checklist

- [ ] Use environment-specific `.env` files
- [ ] Enable HTTPS/SSL with Let's Encrypt
- [ ] Set up monitoring and logging
- [ ] Configure auto-backups
- [ ] Set up CDN for static files
- [ ] Enable rate limiting
- [ ] Configure health checks
- [ ] Set up alerts

### Environment Setup

Create `.env.production`:

```bash
# Backend
OLLAMA_URL=https://ollama.yourdomain.com:11434
DEBUG=false
LOG_LEVEL=info

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
NODE_ENV=production

# Database (if added)
DB_URL=postgresql://user:pass@db:5432/youtube
```

### SSL/TLS Configuration

Using Let's Encrypt with Certbot:

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy to Docker volume
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem

# Update nginx.conf with SSL configuration
# Uncomment SSL section in nginx.conf
```

### Docker Production Best Practices

```yaml
# Add to docker-compose.yml for production
services:
  backend:
    # ... existing config ...
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    resources:
      limits:
        cpus: '1'
        memory: 2G
      reservations:
        cpus: '0.5'
        memory: 1G
```

---

## Monitoring & Logging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# Since specific time
docker-compose logs --since 2024-04-28 backend
```

### Docker Stats

```bash
# Real-time container stats
docker stats

# View container resource usage
docker-compose ps
```

### Health Checks

```bash
# Check service status
curl http://localhost:8000/health
curl http://localhost:3000

# Check Ollama
curl http://localhost:11434/api/tags
```

---

## Troubleshooting

### Issue: "Port already in use"

```bash
# Find process on port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Map to different port
```

### Issue: "Ollama model not found"

```bash
# Pull model manually
docker-compose exec ollama ollama pull mistral

# Check available models
docker-compose exec ollama ollama list
```

### Issue: "Backend can't reach Ollama"

```bash
# Check networking
docker network ls
docker network inspect youtube_youtube-network

# Verify Ollama is running
docker-compose ps

# Test connection from backend
docker-compose exec backend curl http://ollama:11434/api/tags
```

### Issue: "Frontend can't connect to API"

```bash
# Check environment variables
docker-compose exec frontend env | grep REACT_APP_API_URL

# Check network connectivity
docker-compose exec frontend curl http://backend:8000/health

# View frontend logs
docker-compose logs -f frontend
```

### Issue: "Out of memory"

```bash
# Check Docker memory usage
docker system df

# Remove unused images/volumes
docker system prune -a --volumes

# Increase Docker memory allocation
# Settings → Resources → Memory
```

### Issue: "Build fails"

```bash
# Clean build (no cache)
docker-compose build --no-cache

# Check build logs
docker build --no-cache -f backend/Dockerfile backend/ 2>&1 | tail -50
```

---

## Deployment Comparison

| Platform | Cost | Ease | Scaling | Free Tier |
|----------|------|------|---------|-----------|
| Railway | $5-50/mo | ⭐⭐⭐⭐⭐ | Auto | Yes |
| Render | $5-25/mo | ⭐⭐⭐⭐ | Manual | Yes |
| DigitalOcean | $5-50/mo | ⭐⭐⭐ | Manual | No |
| AWS ECS | $10-100+/mo | ⭐⭐ | Auto | Yes (limited) |
| Self-Hosted VPS | $3-20/mo | ⭐⭐⭐ | Manual | No |

---

## Next Steps

1. ✅ Test locally with `docker-compose up`
2. ✅ Push to GitHub
3. ✅ Choose deployment platform
4. ✅ Configure domain and SSL
5. ✅ Set up monitoring
6. ✅ Configure backups

---

## Quick Links

- Docker Docs: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose
- Railway: https://railway.app
- Render: https://render.com
- DigitalOcean: https://www.digitalocean.com

---

**Status**: Ready for deployment ✅  
**Last Updated**: April 29, 2026
