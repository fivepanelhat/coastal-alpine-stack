# Python 3.11 to match pyproject requires-python (>=3.11) and CI.
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
 build-essential \
 curl \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (adjust if needed per service)
EXPOSE 8000

# Default command - adjust based on the actual entrypoint needed
CMD ["python", "-m", "uvicorn", "webhook_relay:app", "--host", "0.0.0.0", "--port", "8000"]
