FROM python:3.11-slim

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install -y wget firefox-esr && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.34.0-linux64.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v0.34.0-linux64.tar.gz

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]