FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install nodemon
RUN apt-get update && apt-get install -y npm && npm install -g nodemon

COPY . .

RUN echo 'alias bot="python3 cli.py"' >> ~/.bashrc

CMD ["nodemon", "--exec", "python", "./main.py"]
