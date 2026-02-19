FROM python:3.14-slim

# Установка системных зависимостей
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     gcc \
     libpq-dev \
     libssl-dev \
     libffi-dev \
     curl \
     ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка uv
RUN pip install --no-cache-dir uv

# Копирование файлов зависимостей
COPY pyproject.toml uv.lock ./

# Установка зависимостей через uv в системный Python (БЕЗ venv)
RUN uv pip install --system --no-cache -r pyproject.toml

# Копирование всего проекта
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]