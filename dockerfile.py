FROM python:3.11-slim

# Cài runtime đa ngôn ngữ
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    g++ \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Tạo working directory
WORKDIR /app

# Copy project
COPY . .

# Cài Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]