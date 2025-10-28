# Multi-stage build for smaller final image
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# Final stage
FROM python:3.10-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ src/
COPY .env.example .env.example

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/src

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default to interactive CLI mode
ENTRYPOINT ["python", "-m", "cli"]

# Allow passing query as arguments for single-query mode
# Usage:
#   docker run <image>                    -> interactive mode
#   docker run <image> --query "text"     -> single query mode
CMD []
