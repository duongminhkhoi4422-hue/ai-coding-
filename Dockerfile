FROM mcr.microsoft.com/devcontainers/universal:2

WORKDIR /app

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy requirements trước để cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

EXPOSE 7860

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]