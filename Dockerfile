FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip uninstall -y telegram telegram-bot python-telegram-bot || true

RUN pip install -r requirements.txt

ENV LD_LIBRARY_PATH=/app/forexconnect/lib

RUN cp forexconnect/fxcorepy.so forexconnect/lib/ || true

RUN cp forexconnect/lib/*.py forexconnect/ || true

CMD ["python", "bot.py"]
