FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

# Remove any conflicting Telegram packages
RUN pip uninstall -y telegram telegram-bot python-telegram-bot || true

# Install dependencies cleanly
RUN pip install --no-cache-dir -r requirements.txt

# FXCM ForexConnect shared libraries
ENV LD_LIBRARY_PATH=/app/forexconnect/lib

# Fix ForexConnect Python package structure
RUN cp forexconnect/fxcorepy.so forexconnect/lib/ || true
RUN cp forexconnect/lib/*.py forexconnect/ || true

CMD ["python", "bot.py"]
