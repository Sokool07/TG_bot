from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL

DIR = Path(__file__).absolute().parent.parent.parent
BOT_DIR = Path(__file__).absolute().parent.parent
LOCALES_DIR = f"{BOT_DIR}/locales"
I18N_DOMAIN = "messages"
DEFAULT_LOCALE = "en"


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class WebhookSettings(EnvBaseSettings):
    USE_WEBHOOK: bool = True  # Включаем webhook для Timeweb Cloud
    WEBHOOK_BASE_URL: str = ""  # Будет установлен через переменные окружения
    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_SECRET: str = ""
    WEBHOOK_HOST: str = "0.0.0.0"  # Слушаем все интерфейсы
    WEBHOOK_PORT: int = 8080  # Порт для Timeweb Cloud

    @property
    def webhook_url(self) -> str:
        if settings.USE_WEBHOOK and self.WEBHOOK_BASE_URL:
            return f"{self.WEBHOOK_BASE_URL}{self.WEBHOOK_PATH}"
        return f"http://{self.WEBHOOK_HOST}:{self.WEBHOOK_PORT}{self.WEBHOOK_PATH}"


class BotSettings(WebhookSettings):
    BOT_TOKEN: str
    CHANNEL_ID: str
    # Удаляем внешние API для Timeweb Cloud
    EMAIL_TOKEN_TTL_MINUTES: int = 15
    INTEGRATIONS_STUB: bool = True  # Включаем заглушки
    SUPPORT_URL: str | None = None
    RATE_LIMIT: int | float = 0.5  # for throttling control
    # Оставляем только miniapp
    FORTUNE_APP_URL: str = "https://fortunewheelsinglefile.netlify.app/"
    NOTCOIN_APP_URL: str = "https://not-coin-mini-app.vercel.app/"


class DBSettings(EnvBaseSettings):
    # Настройки для внутренней БД Timeweb Cloud
    DB_HOST: str = "localhost"  # Будет заменено на внутренний хост Timeweb Cloud
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str | None = None
    DB_NAME: str = "postgres"

    @property
    def database_url(self) -> URL | str:
        if self.DB_PASS:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_psycopg2(self) -> str:
        if self.DB_PASS:
            return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class CacheSettings(EnvBaseSettings):
    # Настройки для внутреннего Redis Timeweb Cloud
    REDIS_HOST: str = "localhost"  # Будет заменено на внутренний хост Timeweb Cloud
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None = None

    # REDIS_DATABASE: int = 1
    # REDIS_USERNAME: int | None = None
    # REDIS_TTL_STATE: int | None = None
    # REDIS_TTL_DATA: int | None = None

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASS:
            return f"redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class Settings(BotSettings, DBSettings, CacheSettings):
    DEBUG: bool = False

    # Отключаем внешние сервисы для Timeweb Cloud
    SENTRY_DSN: str | None = None
    AMPLITUDE_API_KEY: str | None = None  # Отключаем аналитику


settings = Settings()
