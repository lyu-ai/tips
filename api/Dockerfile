# Use official Python 3.12 image from Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the codebase into the working directory
COPY . /app

# Expose port 8842 (for the WebSocket server)
EXPOSE 8842

# Command to run the WebSocket server
CMD ["poetry", "run", "python", "src/main.py"]