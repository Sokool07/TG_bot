# Telegram Bot Template

## Масштабируемый Telegram бот с аналитикой и админ-панелью

Проект Telegram бота с встроенной системой аналитики, мониторинга и администрирования.

## ✨ Основной функционал

- **Админ-панель** - веб-интерфейс для управления ботом на основе Flask-Admin с современным дизайном
- **Система аналитики** - интеграция с популярными сервисами аналитики (Amplitude, PostHog, Google Analytics)
- **Мониторинг производительности** - система мониторинга на базе Prometheus и Grafana
- **Система отслеживания ошибок** - интеграция с Sentry для отслеживания и исправления ошибок
- **Docker контейнеризация** - полная поддержка Docker и Docker Compose для простого развертывания
- **Экспорт данных** - возможность экспорта пользователей в различных форматах (CSV, XLSX, JSON, YAML)
- **База данных** - использование SQLAlchemy V2 для работы с PostgreSQL
- **Миграции БД** - автоматические миграции базы данных через Alembic
- **Кэширование** - система кэширования с использованием Redis
- **Валидация данных** - удобная валидация с помощью Pydantic V2
- **Интернационализация** - поддержка множественных языков через Babel
- **Telegram mini-apps** - Fortune Wheel WebApp и встроенный NotCoin Mini App clone (маршрут `/notcoin/`)

## 🚀 Запуск проекта

### ☁️ Развертывание на Timeweb Cloud (рекомендуемый способ)

1. Подготовьте проект к развертыванию:
   ```bash
   ./scripts/prepare_timeweb_deploy.sh
   ```

2. Настройте переменные окружения в файле `.env.timeweb`

3. Следуйте инструкции в [TIMEWEB_DEPLOYMENT.md](TIMEWEB_DEPLOYMENT.md)

### 🐳 Запуск в Docker (локальная разработка)

1. Настройте переменные окружения в файле `.env`
2. Запустите все сервисы:

    ```bash
    docker compose up -d --build
    ```

### 💻 Запуск на локальной машине

1. Установите зависимости с помощью uv:

    ```bash
    uv sync --frozen --all-groups
    ```

2. Запустите необходимые сервисы (база данных и Redis)

3. Настройте переменные окружения в файле `.env`

4. Запустите Telegram бота:

    ```bash
    uv run python -m bot
    ```

5. Запустите админ-панель:

    ```bash
    uv run gunicorn -c admin/gunicorn_conf.py
    ```

6. Выполните миграции базы данных:

    ```bash
    uv run alembic upgrade head
    ```

### 🎮 Telegram mini-apps

- Fortune Wheel открывается через WebApp по адресу из `FORTUNE_APP_URL` (по умолчанию используется готовый хостинг). Убедитесь, что домен указан в `t.me/botfather` → `Web App`.
- NotCoin mini-app находится в каталоге `webapps/notcoin` и автоматически раздаётся сервисом админ-панели по пути `/notcoin/`. Чтобы обновить сборку:

    ```bash
    cd webapps/notcoin
    npm install
    npm run build
    ```

  После деплоя пропишите домен в BotFather и задайте переменную окружения `NOTCOIN_APP_URL`, например:

    ```env
    NOTCOIN_APP_URL="https://your-domain/notcoin/"
    ```

## 🌍 Environment variables

to launch the bot you only need a token bot, database and redis settings, everything else can be left out

| name                     | description                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `BOT_TOKEN`              | Telegram bot API token                                                                      |
| `RATE_LIMIT`             | Minimum interval in seconds between requests for throttling middleware                      |
| `DEBUG`                  | Enable or disable debugging mode (e.g., `True` or `False`)                                  |
| `USE_WEBHOOK`            | Flag to indicate whether the bot should use a webhook for updates (e.g., `True` or `False`) |
| `WEBHOOK_BASE_URL`       | Base URL for the webhook                                                                    |
| `WEBHOOK_PATH`           | Path to receive updates from Telegram                                                       |
| `WEBHOOK_SECRET`         | Secret key for securing the webhook communication                                           |
| `WEBHOOK_HOST`           | Hostname or IP address for the main application                                             |
| `WEBHOOK_PORT`           | Port number for the main application                                                        |
| `ADMIN_HOST`             | Hostname or IP address for the admin panel                                                  |
| `ADMIN_PORT`             | Port number for the admin panel                                                             |
| `DEFAULT_ADMIN_EMAIL`    | Default email for the admin user                                                            |
| `DEFAULT_ADMIN_PASSWORD` | Default password for the admin user                                                         |
| `SECURITY_PASSWORD_HASH` | Hashing algorithm for user passwords (e.g., `bcrypt`)                                       |
| `SECURITY_PASSWORD_SALT` | Salt value for user password hashing                                                        |
| `DB_HOST`                | Hostname or IP address of the PostgreSQL database                                           |
| `DB_PORT`                | Port number for the PostgreSQL database                                                     |
| `DB_USER`                | Username for authenticating with the PostgreSQL database                                    |
| `DB_PASS`                | Password for authenticating with the PostgreSQL database                                    |
| `DB_NAME`                | Name of the PostgreSQL database                                                             |
| `REDIS_HOST`             | Hostname or IP address of the Redis database                                                |
| `REDIS_PORT`             | Port number for the Redis database                                                          |
| `REDIS_PASS`             | Password for authenticating with the Redis database                                         |
| `FORTUNE_APP_URL`        | URL that opens the Fortune Wheel WebApp                                                     |
| `NOTCOIN_APP_URL`        | URL that opens the NotCoin Mini App                                                         |
| `SENTRY_DSN`             | Sentry DSN (Data Source Name) for error tracking                                            |
| `AMPLITUDE_API_KEY`      | API key for Amplitude analytics                                                             |
| `POSTHOG_API_KEY`        | API key for PostHog analytics                                                               |
| `PROMETHEUS_PORT`        | Port number for the Prometheus monitoring system                                            |
| `GRAFANA_PORT`           | Port number for the Grafana monitoring and visualization platform                           |
| `GRAFANA_ADMIN_USER`     | Admin username for accessing Grafana                                                        |
| `GRAFANA_ADMIN_PASSWORD` | Admin password for accessing Grafana                                                        |

## 📊 Grafana dashboards

The monitoring stack ships with pre-provisioned dashboards that are loaded automatically when you start the `grafana` service
from `docker-compose.yml`:

-   **Node Exporter Full** — reuses the community dashboard for host metrics and is useful for spotting resource starvation
    on the machine that runs the bot.
-   **Telegram Bot Overview** — a custom dashboard that visualizes Prometheus metrics exported by the bot:
    -   request rate grouped by HTTP method (`tgbot_requests`)
    -   response throughput broken down by status code (`tgbot_responses`)
    -   latency quantiles based on the request duration histogram (`tgbot_request_duration_bucket`)
    -   exception rate grouped by exception type (`tgbot_exceptions`)

Once the monitoring stack is running (for example, via `docker compose up grafana prometheus node-exporter`), open
`http://localhost:${GRAFANA_PORT}/d/tgbot-overview/telegram-bot-overview` and log in with the credentials from
`GRAFANA_ADMIN_USER` / `GRAFANA_ADMIN_PASSWORD`. Data refreshes every 30 seconds by
default, so the panels begin to populate as soon as Prometheus scrapes `/metrics` from the bot container.

## 📂 Структура проекта

```bash
.
├── admin/                    # Исходный код админ-панели
│   ├── __init__.py
│   ├── app.py               # Основной модуль приложения админ-панели
│   ├── config.py            # Модуль конфигурации админ-панели
│   ├── Dockerfile           # Dockerfile для админ-панели
│   ├── gunicorn_conf.py     # Конфигурация Gunicorn для админ-панели
│   ├── static/              # Статические ресурсы (CSS, JS, изображения)
│   ├── templates/           # HTML шаблоны для админ-панели
│   └── views/               # Модули представлений для веб-запросов
│
├── bot/                     # Исходный код Telegram бота
│   ├── __init__.py
│   ├── __main__.py          # Точка входа для запуска бота
│   ├── analytics/           # Интеграция с сервисами аналитики
│   ├── cache/               # Логика работы с Redis кэшем
│   ├── core/                # Настройки приложения и основные компоненты
│   ├── database/            # Функции БД и модели SQLAlchemy
│   ├── filters/             # Фильтры для обработки входящих сообщений
│   ├── handlers/            # Обработчики команд и взаимодействий пользователей
│   ├── keyboards/           # Модули создания клавиатур
│   ├── locales/             # Файлы локализации для поддержки языков
│   ├── middlewares/         # Middleware модули для обработки обновлений
│   ├── services/            # Бизнес-логика приложения
│   └── utils/               # Утилиты и вспомогательные модули
│
├── migrations/              # Миграции базы данных (Alembic)
│   ├── env.py               # Настройка окружения для Alembic
│   ├── script.py.mako       # Шаблон скрипта для генерации миграций
│   └── versions/            # Папка с отдельными скриптами миграций
│
├── webapps/                 # Веб-приложения для Telegram WebApp
│   └── notcoin/             # Исходники и сборка NotCoin mini-app (Vite + React)
│
├── configs/                 # Конфигурации мониторинга
│   ├── grafana/             # Конфигурационные файлы Grafana
│   └── prometheus/          # Конфигурационные файлы Prometheus
│
├── scripts/                 # Вспомогательные скрипты
│   └── prepare_timeweb_deploy.sh  # Скрипт подготовки к деплою на Timeweb Cloud
├── Makefile                 # Список команд для стандартных операций
├── alembic.ini              # Конфигурационный файл миграций
├── docker-compose.yml       # Конфигурация Docker Compose (локальная разработка)
├── docker-compose.timeweb.yml  # Конфигурация для Timeweb Cloud
├── Dockerfile               # Dockerfile для Telegram бота
├── timeweb.env              # Переменные окружения для Timeweb Cloud
├── timeweb-env-vars.txt     # Переменные для копирования в панель Timeweb Cloud
├── TIMEWEB_DEPLOYMENT.md    # Инструкция по развертыванию на Timeweb Cloud
├── pyproject.toml           # Конфигурация Python проекта
└── README.md                # Документация
```

## 🔧 Технологический стек

- **SQLAlchemy** — ORM библиотека для работы с реляционными базами данных
- **AsyncPG** — асинхронный клиент для PostgreSQL
- **Aiogram** — асинхронный фреймворк для Telegram Bot API
- **Flask-Admin** — простой и расширяемый фреймворк административного интерфейса
- **Loguru** — библиотека для логирования в Python
- **UV** — современный менеджер пакетов Python
- **Docker** — контейнеризация для автоматизации развертывания
- **PostgreSQL** — мощная объектно-реляционная система управления базами данных
- **PgBouncer** — пулер соединений для PostgreSQL
- **Redis** — хранилище данных в памяти для кэширования и FSM
- **Prometheus** — система мониторинга и база данных временных рядов
- **Grafana** — платформа для визуализации и анализа данных

## 🚀 Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd telegram-bot-template
   ```

2. **Настройте переменные окружения:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env файл с вашими настройками
   ```

3. **Запустите проект в Docker:**
   ```bash
   docker compose up -d --build
   ```

4. **Откройте админ-панель:**
   - URL: http://localhost:5050
   - Логин: admin@example.com
   - Пароль: admin

5. **Откройте Grafana для мониторинга:**
   - URL: http://localhost:3000
   - Логин: admin
   - Пароль: admin

## 📝 Лицензия

Распространяется под лицензией MIT. См. файл LICENSE для получения дополнительной информации.
