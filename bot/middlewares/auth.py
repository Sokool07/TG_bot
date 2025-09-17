from __future__ import annotations
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from bot.services.users import add_user, user_exists
from bot.utils.command import find_command_argument

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        session: AsyncSession = data["session"]
        message: Message = event
        user = message.from_user

        if not user:
            return await handler(event, data)

        try:
            already_exists = await user_exists(session, user.id)
        except SQLAlchemyError as exc:  # table might be missing during bootstrap
            logger.warning(
                "skip auth middleware user check | reason: db error | user_id: {user_id} | err: {error}",
                user_id=user.id,
                error=exc,
            )
            return await handler(event, data)

        if already_exists:
            return await handler(event, data)

        referrer = find_command_argument(message.text)

        logger.info(f"new user registration | user_id: {user.id} | message: {message.text}")

        try:
            await add_user(session=session, user=user, referrer=referrer)
        except SQLAlchemyError as exc:
            logger.warning(
                "failed to add user | user_id: {user_id} | err: {error}",
                user_id=user.id,
                error=exc,
            )
            return await handler(event, data)

        return await handler(event, data)
