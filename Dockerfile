# Use a lightweight, secure Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for ChromaDB and SQLite
RUN apt-get update && apt-get install -y build-essential curl git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy the entire hardened swarm codebase into the container
COPY . .

# Expose the FastAPI Webhook Port
EXPOSE 8000

# Ignite the daemon
CMD ["uvicorn", "webhook_relay:app", "--host", "0.0.0.0", "--port", "8000"]
