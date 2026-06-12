# Base image: ARM64-compatible for the Pi 5
FROM python:3.10-slim-bookworm AS builder

# Enforce strict deterministic behavior and prevent disk-write bloat
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install bare-minimum system dependencies for C++ / NPU bindings
# We immediately purge the apt cache to keep the layer size down
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up the isolated working directory
WORKDIR /opt/coastal_alpine

# Initialize a virtual environment for strict read-only root compatibility
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# CACHE HIT: Copy ONLY the requirements file first.
# This ensures pip install only re-runs if requirements.txt actually changes.
COPY requirements.txt .

# Install production edge dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# --- Future Steps ---
# FROM python:3.10-slim-bookworm AS runner
# COPY --from=builder /opt/venv /opt/venv
# COPY . /opt/coastal_alpine
# ...
