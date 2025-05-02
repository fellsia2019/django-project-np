# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.org/simple

COPY . .

# (используем только для разработки)
RUN if [ "$DJANGO_ENV" = "development" ]; then \
      python manage.py makemigrations && \
      python manage.py migrate; \
    fi

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]