FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

# Remove conflicting Telegram packages
RUN pip uninstall -y telegram telegram-bot python-telegram-bot || true

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# FXCM ForexConnect shared libraries
ENV LD_LIBRARY_PATH=/app/forexconnect/lib

CMD ["python", "bot.py"]
