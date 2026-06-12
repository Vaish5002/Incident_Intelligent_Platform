FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if any are needed (e.g. build-essential for ReportLab or SQLite)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from context
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all backend source files into /app/backend
COPY . /app/backend/

# Set the PYTHONPATH so python finds the backend package in /app
ENV PYTHONPATH=/app

# Expose backend port
EXPOSE 8002

# Run FastAPI app, binding to the PORT environment variable provided by Render
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8002}"]
