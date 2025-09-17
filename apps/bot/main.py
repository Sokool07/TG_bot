from __future__ import annotations

import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from apps.bot.config import settings
from apps.bot.i18n import Translator, get_locale

translator = Translator()


def create_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    @dp.message(CommandStart())
    async def handle_start(message: Message) -> None:  # noqa: D401
        """Entry point for onboarding scenario."""
        locale = get_locale(message.from_user)
        text = translator.gettext("start.welcome", locale=locale)
        await message.answer(text, parse_mode=ParseMode.HTML)

    @dp.message()
    async def handle_fallback(message: Message) -> None:
        locale = get_locale(message.from_user)
        text = translator.gettext("common.unknown_command", locale=locale)
        await message.answer(text)

    return dp


async def main() -> None:
    bot = Bot(token=settings.bot.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = create_dispatcher()

    with suppress(KeyboardInterrupt, TelegramRetryAfter):
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
