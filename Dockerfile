FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/forexconnect

CMD ["python","bot.py"]
