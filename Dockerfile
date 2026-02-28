# ==============================
# Base Image
# ==============================
FROM python:3.11-slim

# ==============================
# Install Multi-Language Runtimes
# ==============================
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    g++ \
    openjdk-17-jdk-headless \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# Set Working Directory
# ==============================
WORKDIR /app

# ==============================
# Install Python Dependencies
# ==============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==============================
# Copy Project Files
# ==============================
COPY . .

# ==============================
# Render uses dynamic PORT
# ==============================
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]