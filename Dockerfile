FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install forexconnect

CMD ["python", "bot.py"]
