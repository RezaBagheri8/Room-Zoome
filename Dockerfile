# Use a specific debian mirror that might be more reliable
FROM python:3.9-slim AS builder

# Set environment variables to reduce noise and avoid interactive prompts
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Use multiple apt mirrors for redundancy
RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80retry && \
    echo 'deb http://ftp.us.debian.org/debian bookworm main' > /etc/apt/sources.list && \
    echo 'deb http://ftp.us.debian.org/debian bookworm-updates main' >> /etc/apt/sources.list && \
    echo 'deb http://security.debian.org/debian-security bookworm-security main' >> /etc/apt/sources.list

# Install minimal build dependencies for WeasyPrint
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    shared-mime-info \
    libffi-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up a virtual environment to isolate dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install WeasyPrint and other dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final image that only contains runtime dependencies
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Use multiple apt mirrors for redundancy
RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80retry && \
    echo 'deb http://ftp.us.debian.org/debian bookworm main' > /etc/apt/sources.list && \
    echo 'deb http://ftp.us.debian.org/debian bookworm-updates main' >> /etc/apt/sources.list && \
    echo 'deb http://security.debian.org/debian-security bookworm-security main' >> /etc/apt/sources.list

# Install only runtime dependencies for WeasyPrint
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
