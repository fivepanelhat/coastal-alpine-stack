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

# --- Final Edge Runner Stage ---
FROM python:3.10-slim-bookworm AS runner

# Enforce environment variables for the edge node execution
ENV PATH="/opt/venv/bin:$PATH" \
 PYTHONDONTWRITEBYTECODE=1 \
 PYTHONUNBUFFERED=1

# SecOps Directive: Create a strictly permissioned, non-root user.
# We absolutely do not run edge inference containers as root.
RUN groupadd -r coastal && useradd -r -g coastal -d /opt/coastal_alpine -s /sbin/nologin coastal

# Set the working directory
WORKDIR /opt/coastal_alpine

# Pull the fully cached, lean virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the monorepo application code, assigning ownership to our restricted user
# Note: Ensure your .dockerignore is ruthless so we don't copy local dev bloat
COPY --chown=coastal:coastal . .

# Drop root privileges immediately
USER coastal

# Define the entrypoint (Update 'main.py' to your actual edge orchestration script)
CMD ["python", "main.py"]
