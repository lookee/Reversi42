# Multi-stage Dockerfile for Reversi42
# Optimized for size and security

# Build argument for version (passed during docker build)
ARG VERSION=5.0.0

# Stage 1: Builder
FROM python:3.11-slim as builder

LABEL maintainer="Luca Amore <luca.amore@gmail.com>"
LABEL description="Reversi42 - Ultra-Fast Reversi/Othello with AI"
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
COPY reversi42 ./reversi42

# Create directories for data
RUN mkdir -p /app/saves /app/tournament/reports

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Set headless by default (no GUI in container)
ENV REVERSI42_VIEW=headless
ENV PYTHONUNBUFFERED=1

# Non-root user for security
RUN useradd -m -u 1000 reversi && \
    chown -R reversi:reversi /app
USER reversi

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import src.Reversi.BitboardGame" || exit 1

# Default command
ENTRYPOINT ["python", "src/reversi42.py"]
CMD ["--view", "headless"]

# Metadata
LABEL org.opencontainers.image.source="https://github.com/lucaamore/reversi42"
LABEL org.opencontainers.image.description="Tournament-grade Reversi/Othello with ultra-fast AI"
LABEL org.opencontainers.image.licenses="GPL-3.0"

