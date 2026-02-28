FROM mcr.microsoft.com/devcontainers/universal:2

WORKDIR /app

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# ❌ Không cần EXPOSE 7860 (Render không cần)

# 🔥 Dùng $PORT của Render
CMD ["sh", "-c", "python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT"]