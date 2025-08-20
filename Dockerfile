# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including NSJail
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    git \
    pkg-config \
    flex \
    bison \
    protobuf-compiler \
    libprotobuf-dev \
    libnl-3-dev \
    libnl-genl-3-dev \
    libnl-route-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install NSJail from source
RUN cd /tmp && \
    git clone https://github.com/google/nsjail.git && \
    cd nsjail && \
    make && \
    cp nsjail /usr/local/bin/ && \
    cd / && \
    rm -rf /tmp/nsjail

# Verify NSJail installation (just check if it exists and is executable)
RUN test -f /usr/local/bin/nsjail && /usr/local/bin/nsjail --help | head -1

# Install Python packages for data science
RUN pip install --no-cache-dir \
    pandas==2.0.3 \
    numpy==1.24.3 \
    scipy==1.11.1

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY api_server.py .
COPY configs/ ./configs/
# Omit copying local scripts/logs/chroot (may be empty/ignored). Directories are created below.

# Create necessary directories
RUN mkdir -p scripts logs chroot

# Set permissions
RUN chmod +x /usr/local/bin/nsjail

# Expose port 8080 (Cloud Run standard)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "api_server:app"]
