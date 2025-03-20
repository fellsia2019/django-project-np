# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.org/simple

# Копируем весь проект
COPY . .

# Собираем статические файлы
RUN python manage.py migrate

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]