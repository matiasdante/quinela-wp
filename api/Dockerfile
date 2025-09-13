# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir gunicorn==22.0.0

# Copy app source
COPY api/ /app/

# Create runtime dirs (DB and logs via volumes preferred)
RUN mkdir -p /app/data /app/logs

# Expose port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://localhost:5000/api/health || exit 1

# Default envs
ENV FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000

# Run with gunicorn for prod
# app object is created in main_api.py as 'app'
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main_api:app"]
