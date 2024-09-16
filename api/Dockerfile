# Use the official Python 3.9 slim image
FROM python:3.9-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies
RUN apt-get update && apt-get install -y \
  ffmpeg \
  build-essential \
  libsndfile1 \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.6.1  # Use a specific version of Poetry

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock for dependency resolution
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies with Poetry (without dev dependencies)
RUN poetry install --no-dev --no-interaction --no-ansi

# Final stage to minimize image size
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
  ffmpeg \
  libsndfile1 \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy only required files from builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Expose the WebSocket port
EXPOSE 8842

# Command to run the WebSocket server
CMD ["poetry", "run", "python", "src/main.py"]