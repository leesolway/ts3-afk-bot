FROM python:3.8-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]
