# Use NVIDIA CUDA base as the parent image to ensure libraries are available if needed
# We use the runtime version to keep it smaller while having CUDA support
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
# ffmpeg is STRICTLY required for Whisper/pydub
# libpq-dev is required for psycopg2 (PostgreSQL)
# We also install python3 and pip since they aren't in the cuda base image
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    ffmpeg \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set python3 as default python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set work directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml .
COPY README.md .
COPY main.py .
COPY database.py .
COPY transcriber.py .

# Smart installation: Detect CUDA presence at build time
# If the build node has access to the GPU or is configured with nvidia runtime,
# we install the CUDA-optimized PyTorch. Otherwise, we install the standard version.
# Note: In most CI/CD or local builds without --gpus all, this will fallback to standard torch.
RUN if command -v nvidia-smi > /dev/null 2>&1 || [ -f /proc/driver/nvidia/version ]; then \
    echo "CUDA detected! Installing CUDA-enabled PyTorch..." && \
    pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cu118; \
    else \
    echo "No CUDA detected at build time. Installing standard PyTorch..."; \
    fi

# Install the rest of the dependencies and the package itself
RUN pip install --no-cache-dir .

# Create directory for recordings
RUN mkdir -p /recordings

# Default environment variables (can be overridden)
ENV DATABASE_URL=""
ENV WHISPER_MODEL="base"
ENV WHISPER_DEVICE="cpu"
ENV RECORDINGS_PATH="/recordings"

# Entry point
CMD ["python", "main.py"]
