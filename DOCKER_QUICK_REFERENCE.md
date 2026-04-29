# 🐳 Docker Quick Reference - YouTube Analyzer

## Start Deploying in 30 Seconds

### Option A: Interactive Script (Easiest)

```bash
cd /Users/viyangchaudhari/Projects/youtube
./deploy.sh
```

Then select option `1` and follow prompts.

### Option B: Manual Commands

```bash
cd /Users/viyangchaudhari/Projects/youtube

# Start all services
docker-compose up -d

# Wait for Ollama to download model (first time only, takes 5-10 minutes)
docker-compose exec ollama ollama pull mistral

# Access your app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 📊 What Gets Started

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Frontend | 3000 | http://localhost:3000 | Web interface |
| Backend | 8000 | http://localhost:8000 | API server |
| API Docs | 8000 | http://localhost:8000/docs | Interactive docs |
| Ollama | 11434 | http://localhost:11434 | LLM inference engine |

---

## ⚡ Common Commands

```bash
# Status
docker-compose ps

# Logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ollama

# Stop
docker-compose stop

# Start again
docker-compose start

# Remove everything
docker-compose down -v

# Rebuild
docker-compose build --no-cache
```

---

## 🌐 Deploy Online (Choose One)

### Railway (Easiest) ⭐

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your `youtube` repo
4. Done! It auto-detects `docker-compose.yml`

**Result**: Your app at `https://your-project.railway.app`

### AWS/DigitalOcean/Render

See `DOCKER_DEPLOYMENT_GUIDE.md` for detailed instructions.

---

## 🔧 Troubleshooting

### "Port 8000 already in use"
```bash
lsof -i :8000
kill -9 <PID>
# Or change port in docker-compose.yml
```

### "Ollama not working"
```bash
docker-compose exec ollama ollama pull mistral
docker-compose restart backend
```

### "Frontend can't reach backend"
```bash
docker-compose exec frontend curl http://backend:8000/health
```

### "Services won't start"
```bash
# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

## 📁 Files Created

```
✅ backend/Dockerfile
✅ frontend/Dockerfile
✅ docker-compose.yml
✅ nginx.conf
✅ deploy.sh
✅ DOCKER_DEPLOYMENT_GUIDE.md
✅ DOCKER_QUICK_REFERENCE.md (this file)
```

---

## 🚀 Next Steps

### Local Testing
```bash
./deploy.sh        # Or docker-compose up -d
# Open http://localhost:3000 in browser
```

### Deploy Online
1. Commit and push to GitHub
2. Go to https://railway.app
3. Connect GitHub repo
4. Click deploy!

---

## 💡 Pro Tips

- **First run takes 10-15 minutes** - Ollama downloads the 4GB mistral model
- **Use `./deploy.sh`** - Interactive menu is easier than remembering commands
- **Check logs if something fails** - `docker-compose logs -f`
- **Health checks** - Backend has `/health` endpoint, use it to verify status
- **SSL/TLS** - Use Railway or similar for automatic HTTPS

---

## 📞 Need Help?

- Docker: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose
- Full guide: `DOCKER_DEPLOYMENT_GUIDE.md`
- Troubleshooting: See section above

---

**Ready to deploy?** Run: `./deploy.sh` 🚀
