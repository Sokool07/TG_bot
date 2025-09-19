#!/bin/bash

# Скрипт для подготовки к развертыванию на Timeweb Cloud

set -e

echo "🚀 Подготовка к развертыванию на Timeweb Cloud..."

# Проверяем наличие необходимых файлов
echo "📋 Проверка файлов..."

if [ ! -f "docker-compose.timeweb.yml" ]; then
    echo "❌ Файл docker-compose.timeweb.yml не найден!"
    exit 1
fi

if [ ! -f "timeweb.env" ]; then
    echo "❌ Файл timeweb.env не найден!"
    exit 1
fi

if [ ! -f "Dockerfile" ]; then
    echo "❌ Файл Dockerfile не найден!"
    exit 1
fi

echo "✅ Все необходимые файлы найдены"

# Создаем .env.timeweb из timeweb.env
echo "📝 Создание .env.timeweb..."
cp timeweb.env .env.timeweb
echo "✅ Файл .env.timeweb создан"

# Проверяем, что все обязательные переменные заполнены
echo "🔍 Проверка переменных окружения..."

# Список обязательных переменных
REQUIRED_VARS=(
    "BOT_TOKEN"
    "CHANNEL_ID"
    "WEBHOOK_BASE_URL"
    "WEBHOOK_SECRET"
    "DB_PASS"
    "REDIS_PASS"
    "DEFAULT_ADMIN_PASSWORD"
    "SECRET_KEY"
)

MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if grep -q "^${var}=your_.*_here$" .env.timeweb; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "⚠️  Внимание! Следующие переменные не заполнены:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "📝 Отредактируйте файл .env.timeweb перед развертыванием"
    echo ""
fi

# Проверяем Docker
echo "🐳 Проверка Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi

# Проверяем Docker Compose (может быть как отдельная команда или как подкоманда docker)
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose не установлен!"
    exit 1
fi

echo "✅ Docker и Docker Compose доступны"

# Тестируем сборку образа
echo "🔨 Тестирование сборки образа..."
if docker build -t tgbot-test . > /dev/null 2>&1; then
    echo "✅ Образ собирается успешно"
    docker rmi tgbot-test > /dev/null 2>&1
else
    echo "❌ Ошибка при сборке образа!"
    echo "Запустите 'docker build -t tgbot-test .' для диагностики"
    exit 1
fi

# Проверяем docker-compose файл
echo "📋 Проверка docker-compose.timeweb.yml..."
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

if $COMPOSE_CMD -f docker-compose.timeweb.yml config > /dev/null 2>&1; then
    echo "✅ docker-compose.timeweb.yml корректен"
else
    echo "❌ Ошибка в docker-compose.timeweb.yml!"
    echo "Запустите '$COMPOSE_CMD -f docker-compose.timeweb.yml config' для диагностики"
    exit 1
fi

echo ""
echo "🎉 Подготовка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте файл .env.timeweb с вашими настройками"
echo "2. Загрузите код в Git репозиторий"
echo "3. Создайте приложение в Timeweb Cloud"
echo "4. Подключите репозиторий и укажите docker-compose.timeweb.yml"
echo "5. Добавьте переменные окружения из .env.timeweb"
echo "6. Запустите деплой"
echo ""
echo "📖 Подробная инструкция: TIMEWEB_DEPLOYMENT.md"
