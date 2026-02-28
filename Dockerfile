FROM openjdk:17-jdk-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Python, C++, Node
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        g++ \
        nodejs \
        npm \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Make python command available
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]