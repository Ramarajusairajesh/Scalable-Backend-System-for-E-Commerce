# syntax=docker/dockerfile:1
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pytest-asyncio

# Copy source code and migrations
COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini .

# Create entrypoint script
RUN echo '#!/bin/sh\n\
echo "Waiting for PostgreSQL..."\n\
while ! nc -z postgres 5432; do\n\
  echo "PostgreSQL is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
echo "PostgreSQL started"\n\
\n\
echo "Running database migrations..."\n\
export PYTHONPATH=/app\n\
alembic upgrade head || {\n\
  echo "Migration failed!"\n\
  exit 1\n\
}\n\
echo "Migrations completed successfully"\n\
\n\
echo "Starting API service..."\n\
exec uvicorn src.api_service.main:app --host 0.0.0.0 --port 8000\n' > /app/entrypoint.sh && \
chmod +x /app/entrypoint.sh

# Set Python path
ENV PYTHONPATH=/app

EXPOSE 8000

# Copy tests
COPY tests/ ./tests/

# Default command runs tests
CMD ["pytest", "tests"] 