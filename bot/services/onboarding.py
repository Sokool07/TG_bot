from __future__ import annotations
from dataclasses import dataclass

from loguru import logger

from bot.core.config import settings


@dataclass(slots=True)
class StartLinkingResult:
    email: str
    casino_user_id: str | None = None


@dataclass(slots=True)
class BonusGrantResult:
    success: bool
    reason: str | None = None


async def start_linking(telegram_id: int, identifier: str) -> StartLinkingResult:
    """Call WS/SV API to find casino account and persist pending link."""
    if settings.INTEGRATIONS_STUB:
        email = identifier if "@" in identifier else f"{identifier}@example.com"
        return StartLinkingResult(email=email)

    logger.warning("start_linking integration not implemented", telegram_id=telegram_id)
    raise NotImplementedError


async def confirm_token(telegram_id: int, token: str) -> str:  # noqa: ARG001
    """Validate token provided by user."""
    if settings.INTEGRATIONS_STUB:
        return f"casino-{telegram_id}"

    logger.warning("confirm_token integration not implemented", telegram_id=telegram_id)
    raise NotImplementedError


async def grant_bonus(telegram_id: int, casino_user_id: str) -> BonusGrantResult:
    """Grant bonus after verifying all conditions."""
    if settings.INTEGRATIONS_STUB:
        return BonusGrantResult(success=True)

    logger.warning(
        "grant_bonus integration not implemented",
        telegram_id=telegram_id,
        casino_user_id=casino_user_id,
    )
    raise NotImplementedError
