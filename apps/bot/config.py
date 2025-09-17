from __future__ import annotations

from functools import lru_cache

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: SecretStr = Field(alias="BOT_TOKEN")
    channel_id: str = Field(alias="CHANNEL_ID")

    api_base_url: str = Field(default="http://api:8000", alias="API_BASE_URL")
    ws_sv_api_url: str = Field(alias="WS_SV_API_URL")
    ws_sv_api_key: SecretStr = Field(alias="WS_SV_API_KEY")

    gbl_bonus_api_url: str = Field(alias="GBL_BONUS_API_URL")
    gbl_bonus_api_key: SecretStr = Field(alias="GBL_BONUS_API_KEY")

    integrations_stub: bool = Field(default=False, alias="INTEGRATIONS_STUB")
    locale_default: str = Field(default="ru", alias="LOCALE_DEFAULT")


class Settings(BaseModel):
    bot: BotSettings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    bot_settings = BotSettings()  # type: ignore[call-arg]
    return Settings(bot=bot_settings)


settings = get_settings()
