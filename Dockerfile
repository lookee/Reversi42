# Multi-stage Dockerfile for Reversi42 WebGUI
# Optimized for size and security

# Build argument for version
ARG VERSION=6.0.0

# Stage 1: Builder
FROM python:3.11-slim as builder

LABEL maintainer="Luca Amore <luca.amore@gmail.com>"
LABEL description="Reversi42 - Ultra-Fast Reversi/Othello Web Game with AI"
LABEL version="${VERSION}"

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/src:/app
ENV PYTHONUNBUFFERED=1

# Non-root user for security
RUN useradd -m -u 1000 reversi && \
    chown -R reversi:reversi /app
USER reversi

# Expose web server port
EXPOSE 8000

# Health check - simple Python import test
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import sys; sys.path.insert(0, '/app/src'); from Reversi.BitboardGame import BitboardGame" || exit 1

# Start web server directly
CMD ["python", "src/webgui/server/reversi42_server.py", "--port", "8000", "--host", "0.0.0.0", "--player", "DIVZERO.EXE"]

# Metadata
LABEL org.opencontainers.image.source="https://github.com/lookee/reversi42"
LABEL org.opencontainers.image.description="Tournament-grade Reversi/Othello web game with ultra-fast AI"
LABEL org.opencontainers.image.licenses="GPL-3.0"
LABEL org.opencontainers.image.url="https://github.com/lookee/reversi42"
LABEL org.opencontainers.image.documentation="https://github.com/lookee/reversi42/blob/main/README.md"
