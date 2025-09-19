# ⚡ Быстрый старт на Timeweb Cloud

## 🚀 За 5 минут

### 1. Подготовка
```bash
# Скопируйте файл с переменными
cp env.example .env

# Отредактируйте .env файл
nano .env
```

### 2. Обязательные переменные
```env
BOT_TOKEN=your_bot_token_here
CHANNEL_ID=@your_channel_username
WEBHOOK_BASE_URL=https://your-app-name.timeweb.cloud
DB_HOST=your_postgres_host
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=your_db_name
REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_PASS=your_redis_password
```

### 3. Развертывание
1. Зайдите на [timeweb.cloud](https://timeweb.cloud)
2. Создайте приложение типа **Dockerfile**
3. Подключите ваш Git репозиторий
4. Добавьте переменные окружения из `.env`
5. Запустите деплой

### 4. Настройка webhook
```bash
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-app-name.timeweb.cloud/webhook"}'
```

### 5. Проверка
```bash
# Health check
curl https://your-app-name.timeweb.cloud/health

# Статус webhook
curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"
```

## ✅ Готово!

Ваш бот теперь работает на Timeweb Cloud! 

📖 **Подробная документация**: [TIMEWEB_DEPLOY.md](./TIMEWEB_DEPLOY.md)
