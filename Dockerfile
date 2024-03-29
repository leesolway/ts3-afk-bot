FROM python:3.10-slim

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo 'alias bot="python3 cli.py"' >> ~/.bashrc

CMD ["python", "main.py"]
