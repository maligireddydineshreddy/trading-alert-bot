FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libssl-dev \
    libboost-system1.74.0 \
    libboost-python1.74.0 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app/forexconnect

CMD ["python","bot.py"]
