# Use NVIDIA CUDA base image if you plan to use GPU, 
# otherwise a standard python image works.
# For Whisper, a Debian-based image is better for FFmpeg compatibility.
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# ffmpeg is STRICTLY required for Whisper/pydub
# libpq-dev is required for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libpq-dev \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml .
COPY README.md .
COPY main.py .
COPY database.py .
COPY transcriber.py .

# Install dependencies
# Using --no-cache-dir to keep the image small
RUN pip install --no-cache-dir .

# Create directory for recordings (to be mounted as a volume)
RUN mkdir -p /recordings

# Default environment variables (can be overridden)
ENV DATABASE_URL=""
ENV WHISPER_MODEL="base"
ENV WHISPER_DEVICE="cpu"
ENV RECORDINGS_PATH="/recordings"

# Entry point
CMD ["python", "main.py"]
