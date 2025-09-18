from __future__ import annotations

import time
from alembic import command
from alembic.config import Config
from loguru import logger

from bot.core.config import DIR, settings


def _configure_alembic() -> Config:
    config_path = DIR / "alembic.ini"
    migrations_path = DIR / "migrations"

    alembic_cfg = Config(str(config_path))
    alembic_cfg.set_main_option("script_location", str(migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.database_url))

    return alembic_cfg


def run_migrations(max_attempts: int = 5, delay_seconds: float = 2.0) -> None:
    """Apply pending migrations before starting the bot."""

    alembic_cfg = _configure_alembic()

    for attempt in range(1, max_attempts + 1):
        try:
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migrations applied")
            return
        except Exception as exc:  # noqa: BLE001
            if attempt == max_attempts:
                logger.exception("Failed to apply database migrations")
                raise

            logger.warning(
                "Migration attempt {attempt}/{max_attempts} failed: {error}. Retrying in {delay}s...",
                attempt=attempt,
                max_attempts=max_attempts,
                error=exc,
                delay=delay_seconds,
            )
            time.sleep(delay_seconds)
