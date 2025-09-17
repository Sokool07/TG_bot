from __future__ import annotations

from functools import lru_cache

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default="tg-onboarding-api", alias="APP_NAME")
    debug: bool = Field(default=False, alias="DEBUG")

    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")

    db_url: SecretStr = Field(alias="DB_URL")

    ws_sv_api_url: str = Field(alias="WS_SV_API_URL")
    ws_sv_api_key: SecretStr = Field(alias="WS_SV_API_KEY")

    customerio_api_key: SecretStr = Field(alias="CUSTOMERIO_API_KEY")

    gbl_bonus_api_url: str = Field(alias="GBL_BONUS_API_URL")
    gbl_bonus_api_key: SecretStr = Field(alias="GBL_BONUS_API_KEY")

    integrations_stub: bool = Field(default=False, alias="INTEGRATIONS_STUB")
    email_token_ttl_minutes: int = Field(default=15, alias="EMAIL_TOKEN_TTL_MINUTES")


class Settings(BaseModel):
    api: ApiSettings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    api_settings = ApiSettings()  # type: ignore[call-arg]
    return Settings(api=api_settings)


settings = get_settings()
