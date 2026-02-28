FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    g++ \
    openjdk-17-jre-headless \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]