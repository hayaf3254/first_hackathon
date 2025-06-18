# backend/Dockerfile にある前提の書き方
FROM python:3.11-slim-buster

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* 

WORKDIR /app

# ✅ ここは backend/ じゃなくて単に "requirements.txt"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ backend 配下の全ソースをコピー
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
