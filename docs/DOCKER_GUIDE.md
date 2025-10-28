# 🐳 Docker Guide

Complete guide for running the LangGraph Supervised Quickstart in Docker containers.

---

## 📦 Quick Start

### Prerequisites
- Docker 20.10+ installed
- Docker Compose v2+ (optional but recommended)
- `.env` file configured with your API keys

### Basic Usage

**Interactive mode (default):**
```bash
docker compose up --build
```

**Single query mode:**
```bash
docker run --env-file .env langgraph-quickstart --query "Extract entities from: Tesla and SpaceX"
```

---

## 🏗️ Build & Run

### Using Docker Compose (Recommended)

**1. Build the image:**
```bash
docker compose build
```

**2. Run interactive mode:**
```bash
docker compose up
```

**3. Run single-query mode:**
```bash
docker compose run --rm langgraph-quickstart --query "Calculate stats for: 10, 20, 30"
```

**4. Stop and clean up:**
```bash
docker compose down
```

### Using Docker Directly

**1. Build the image:**
```bash
docker build -t langgraph-quickstart:latest .
```

**2. Run interactive mode:**
```bash
docker run -it --rm \
  --env-file .env \
  langgraph-quickstart:latest
```

**3. Run single-query mode:**
```bash
docker run --rm \
  --env-file .env \
  langgraph-quickstart:latest \
  --query "Analyze text: OpenAI and LangGraph"
```

---

## ⚙️ Configuration

### Environment Variables

The container reads from your `.env` file. Make sure it contains:

```bash
# Required
OPENAI_API_KEY=sk-proj-your-key-here

# Optional
LANGSMITH_API_KEY=lsv2-your-key-here
LANGSMITH_TRACING=true
OPENAI_MODEL=gpt-4o-mini
CLI_ASCII_BANNER=true
DEBUG=true
```

### Passing Environment Variables

**Option 1: Using .env file (recommended):**
```bash
docker run -it --env-file .env langgraph-quickstart
```

**Option 2: Inline environment variables:**
```bash
docker run -it \
  -e OPENAI_API_KEY=sk-proj-... \
  -e LANGSMITH_API_KEY=lsv2-... \
  langgraph-quickstart
```

**Option 3: Using Docker Compose:**
```yaml
# docker compose.yml already configured
env_file:
  - .env
```

---

## 🔧 Advanced Usage

### Development Mode (Hot Reload)

Mount your `src/` directory to develop without rebuilding:

```bash
docker run -it --rm \
  --env-file .env \
  -v $(pwd)/src:/app/src:ro \
  langgraph-quickstart
```

Or using Docker Compose (uncomment in `docker compose.yml`):
```yaml
volumes:
  - ./src:/app/src:ro
```

### Resource Limits

**Using Docker run:**
```bash
docker run -it --rm \
  --env-file .env \
  --memory=512m \
  --cpus=1 \
  langgraph-quickstart
```

**Using Docker Compose (already configured):**
```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
```

### Custom Network

```bash
# Create network
docker network create langgraph-net

# Run with custom network
docker run -it --rm \
  --env-file .env \
  --network langgraph-net \
  --name langgraph-app \
  langgraph-quickstart
```

---

## 📊 Multi-Stage Build

The Dockerfile uses a multi-stage build for optimization:

**Stage 1 (builder):** Compiles dependencies with build tools
**Stage 2 (final):** Minimal runtime image (~200MB vs ~500MB)

**Benefits:**
- ✅ Smaller final image size
- ✅ Faster deployment
- ✅ Reduced attack surface
- ✅ No unnecessary build tools in production

---

## 🧪 Testing in Docker

### Run a quick test:
```bash
docker run --rm \
  --env-file .env \
  langgraph-quickstart \
  --query "Test query: extract entities from Docker and Kubernetes"
```

### Expected output:
```
╭────────────── Query ──────────────╮
│ Test query: extract entities...   │
╰────────────────────────────────────╯

🤔 Processing...

╭──────────── ✨ Response ──────────╮
│ Entities extracted:               │
│ • Docker                          │
│ • Kubernetes                      │
╰────────────────────────────────────╯
```

---

## 🐞 Debugging

### View container logs:
```bash
docker compose logs -f
```

### Interactive shell in container:
```bash
docker run -it --rm \
  --env-file .env \
  --entrypoint /bin/bash \
  langgraph-quickstart
```

### Check Python environment:
```bash
docker run --rm langgraph-quickstart python --version
docker run --rm langgraph-quickstart pip list
```

### Enable debug mode:
```bash
docker run -it --rm \
  --env-file .env \
  -e DEBUG=true \
  langgraph-quickstart
```

---

## 📝 Docker Compose Profiles

The `docker compose.yml` includes a separate service for single-query mode using profiles:

**Run single-query service:**
```bash
docker compose --profile single-query run langgraph-single-query
```

**Or override the command:**
```bash
docker compose run --rm langgraph-quickstart \
  --query "Your custom query here"
```

---

## 🔒 Security Best Practices

### 1. Never commit .env files
```bash
# Already in .gitignore
.env
.env.local
```

### 2. Use secrets management in production
```bash
# Docker Swarm secrets
docker secret create openai_key /path/to/key.txt

# Kubernetes secrets
kubectl create secret generic api-keys \
  --from-literal=OPENAI_API_KEY=sk-proj-...
```

### 3. Run as non-root user (optional enhancement)
```dockerfile
# Add to Dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 4. Scan for vulnerabilities
```bash
docker scan langgraph-quickstart:latest
```

---

## 📦 Image Management

### Tag and version:
```bash
docker build -t langgraph-quickstart:0.1.0 .
docker build -t langgraph-quickstart:latest .
```

### Push to registry:
```bash
# Docker Hub
docker tag langgraph-quickstart:latest your-username/langgraph-quickstart:latest
docker push your-username/langgraph-quickstart:latest

# GitHub Container Registry
docker tag langgraph-quickstart:latest ghcr.io/joaomede/langgraph-quickstart:latest
docker push ghcr.io/joaomede/langgraph-quickstart:latest
```

### Clean up:
```bash
# Remove unused images
docker image prune -a

# Remove specific image
docker rmi langgraph-quickstart:latest
```

---

## 🚀 Production Deployment

### Docker Swarm:
```bash
docker stack deploy -c docker compose.yml langgraph
```

### Kubernetes:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langgraph-quickstart
spec:
  replicas: 1
  selector:
    matchLabels:
      app: langgraph
  template:
    metadata:
      labels:
        app: langgraph
    spec:
      containers:
      - name: langgraph
        image: langgraph-quickstart:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
        resources:
          limits:
            memory: "512Mi"
            cpu: "1000m"
```

---

## 🔍 Healthcheck

The Dockerfile includes a basic healthcheck:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"
```

**Check health status:**
```bash
docker ps
# Look for "healthy" in STATUS column
```

**Custom healthcheck:**
```dockerfile
HEALTHCHECK --interval=10s CMD python -c "from cli import _check_env; _check_env()" || exit 1
```

---

## ❓ Troubleshooting

### Issue: Container exits immediately
**Solution:** Make sure you're running in interactive mode:
```bash
docker run -it --env-file .env langgraph-quickstart
```

### Issue: Environment variables not loaded
**Solution:** Check .env file exists and has correct format:
```bash
cat .env
docker run --rm --env-file .env langgraph-quickstart env | grep OPENAI
```

### Issue: Permission denied
**Solution:** Check .env file permissions:
```bash
chmod 600 .env
```

### Issue: Out of memory
**Solution:** Increase Docker memory limit:
```bash
# Docker Desktop: Settings > Resources > Memory
docker run -it --rm --memory=1g langgraph-quickstart
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Need help?** [Open an issue](https://github.com/joaomede/langgraph-supervised-quickstart/issues) or check the main [README](../README.md).
