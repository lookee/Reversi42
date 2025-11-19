# Dockerfile for Reversi42 WebGUI
FROM python:3.11-slim

LABEL maintainer="Luca Amore <luca.amore@gmail.com>"
LABEL description="Reversi42 - AI-Powered Reversi/Othello Web Game"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/

# Add src to Python path
ENV PYTHONPATH=/app/src:/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Non-root user
RUN useradd -m -u 1000 reversi && \
    chown -R reversi:reversi /app
USER reversi

# Simple healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD python -c "import sys; sys.path.insert(0, '/app/src'); import Reversi" || exit 1

# Start server (direct Python execution)
WORKDIR /app/src
CMD ["python", "-m", "webgui.server.reversi42_server", "--port", "8000", "--host", "0.0.0.0", "--player", "DIVZERO.EXE"]

# Metadata
LABEL org.opencontainers.image.source="https://github.com/lookee/Reversi42"
LABEL org.opencontainers.image.description="Tournament-grade Reversi/Othello web game with AI"
LABEL org.opencontainers.image.licenses="GPL-3.0"
