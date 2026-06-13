FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed by ReportLab (PDF) and scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# IMPORTANT: Docker Build Context must be set to: Project/backend
# Dockerfile path:                               Project/backend/Dockerfile
# Both paths are configured in render.yaml and Render Dashboard.
# ------------------------------------------------------------------

# Step 1: Copy and install Python dependencies first (for layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Step 2: Copy all backend source files into /app/backend/
#         (context root = Project/backend/, so "." = all files there)
COPY . /app/backend/

# Step 3: Set PYTHONPATH so "from backend.xxx import yyy" resolves correctly
ENV PYTHONPATH=/app

# Expose default port (Render overrides with $PORT at runtime)
EXPOSE 8002

# Step 4: Start FastAPI with Render's dynamic $PORT (fallback to 8002 locally)
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8002}"]
