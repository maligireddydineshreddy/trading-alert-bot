FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install \
    python-telegram-bot \
    numpy \
    pandas \
    requests

RUN pip install -r requirements.txt

ENV LD_LIBRARY_PATH=/app/forexconnect/lib:$LD_LIBRARY_PATH

CMD ["python", "bot.py"]
