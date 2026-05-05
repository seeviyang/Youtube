# 🐳 Docker Daemon Not Running - Fix Guide

## Error You Got

```
unable to get image 'youtube-backend': Cannot connect to the Docker daemon 
at unix:///Users/viyangchaudhari/.docker/run/docker.sock. Is the docker daemon running?
```

**This means**: Docker daemon is not running on your system.

---

## ✅ Solution

### Step 1: Start Docker Desktop

**On macOS:**

1. Open **Finder**
2. Go to **Applications** folder
3. Find **Docker.app**
4. Double-click to launch it

**Or use Spotlight:**
```bash
⌘ + Space
Type: Docker
Press Enter
```

### Step 2: Wait for Docker to Start

Docker may take 30-60 seconds to fully start. You'll see the Docker icon in the menu bar turn solid when ready.

### Step 3: Verify Docker is Running

```bash
docker --version
```

**Expected output:**
```
Docker version 24.0.0 (or similar)
```

### Step 4: Check Docker Daemon Status

```bash
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

(Empty list is fine - it just means no containers are running)

---

## 🐛 If Docker Still Won't Start

### Check if Docker is installed

```bash
which docker
```

**If nothing shows**: Docker is not installed.

**Fix**: Download from https://www.docker.com/products/docker-desktop

### Check Docker logs

```bash
# View Docker logs
log stream --predicate 'process == "Docker"'

# Or check system log
tail -f /var/log/system.log | grep -i docker
```

### Restart Docker daemon

```bash
# Option 1: Use UI
# Click Docker icon in menu bar → Quit Docker
# Wait 10 seconds
# Open Docker.app again

# Option 2: Command line
killall Docker
sleep 5
open /Applications/Docker.app
```

### Reset Docker (last resort)

⚠️ **Warning**: This removes all containers and images!

```bash
# Open Docker Desktop
# Settings → General → Reset Docker Desktop
# Click "Reset"
```

---

## ✅ Once Docker is Running

### Try deployment script again

```bash
cd /Users/viyangchaudhari/Projects/youtube
./deploy.sh
```

Select option `1` and services should start!

### Or use docker-compose directly

```bash
docker-compose up -d
```

### Verify services started

```bash
docker-compose ps
```

**Expected output:**
```
CONTAINER ID   IMAGE              STATUS          PORTS
xxx            youtube-backend    Up 2 minutes    0.0.0.0:8000->8000/tcp
xxx            youtube-frontend   Up 2 minutes    0.0.0.0:3000->3000/tcp
xxx            ollama             Up 2 minutes    0.0.0.0:11434->11434/tcp
```

---

## 🔧 Docker Desktop Settings (macOS)

### Recommended Settings

1. **Open Docker Desktop**
2. **Click Docker icon** → **Preferences** (or Settings)
3. **General Tab**:
   - ✅ "Start Docker Desktop when you log in"
   - ✅ "Use containerd for pulling and storing images"
   - ✅ "Use gRPC FUSE for file sharing"

4. **Resources Tab**:
   - **CPUs**: Set to at least 2
   - **Memory**: Set to at least 4GB (8GB recommended)
   - **Disk**: Set to 50GB or more
   - **Swap**: 1GB minimum

5. **File Sharing Tab**:
   - Add `/Users/viyangchaudhari/Projects/youtube`
   - This allows containers to access your project

### Check Current Settings

```bash
docker info | grep -E "Memory|CPUs|Storage"
```

---

## 🆘 Common Issues

### "Cannot connect to Docker daemon"

**Cause**: Docker Desktop not running

**Fix**:
```bash
# Start Docker
open /Applications/Docker.app

# Wait 30 seconds, then try:
docker ps
```

### "Docker command not found"

**Cause**: Docker not installed

**Fix**:
1. Download from: https://www.docker.com/products/docker-desktop
2. Install and run Docker.app
3. Try again

### "Permission denied while trying to connect to Docker socket"

**Cause**: User not in docker group

**Fix**:
```bash
# Add current user to docker group
sudo dscl . -append /Groups/docker GroupMembership $(whoami)

# Or use sudo
sudo docker ps
```

### "docker-compose: command not found"

**Cause**: Docker Compose not installed

**Fix**:
```bash
# Install via Docker Desktop (comes with it)
# Or install standalone:
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### "Port 8000 already in use"

**Cause**: Another service using that port

**Fix**:
```bash
# Find what's using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port in docker-compose.yml:
ports:
  - "8001:8000"
```

---

## 📋 Step-by-Step Checklist

- [ ] Docker Desktop installed
- [ ] Docker Desktop is running (check menu bar)
- [ ] `docker --version` shows version
- [ ] `docker ps` shows empty list
- [ ] Docker has enough resources (2+ CPUs, 4+ GB RAM)
- [ ] `/Users/viyangchaudhari/Projects/youtube` is in file sharing
- [ ] Run `./deploy.sh` again
- [ ] Services start successfully

---

## 🚀 Once Everything Works

### Access your application

```bash
# After services start
docker-compose ps

# Open browser to:
http://localhost:3000          # Frontend
http://localhost:8000          # Backend
http://localhost:8000/docs     # API Documentation
```

### Monitor logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f ollama
```

### Stop services

```bash
docker-compose down
```

---

## 💡 Pro Tips

- **Docker takes time to start**: First run may take 5-10 minutes (Ollama downloads 4GB model)
- **Keep Docker running**: Easier than restarting each time
- **Watch the logs**: Always check `docker-compose logs` if something fails
- **Increase resources**: More RAM = faster container startup
- **File permissions**: Add your project path to Docker's file sharing

---

## 📞 Need More Help?

- Docker Docs: https://docs.docker.com/desktop/install/mac/
- Docker Community: https://forums.docker.com
- Your specific error: Search the error message on StackOverflow

---

**Next**: Once Docker is running, run: `./deploy.sh` 🚀

