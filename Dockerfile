FROM python:3.11-slim

# ffmpeg va kerakli tizim kutubxonalarini o'rnatish
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads output

# Render PORT o'zgaruvchisini beradi, shuni ishlatamiz
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 600
