FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Сначала копируем только requirements.txt для кэширования слоев
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем остальные файлы проекта
COPY . .

# Компилируем локализацию
RUN pybabel compile -d ./bot/locales

# Создаем пользователя для безопасности
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

USER appuser

# Открываем порт для Timeweb Cloud
EXPOSE 8080

# Запускаем бота
CMD ["python", "-m", "bot"]
