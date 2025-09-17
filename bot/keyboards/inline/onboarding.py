from __future__ import annotations

from urllib.parse import quote

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CHECK_CALLBACK_DATA = "onboarding:check"


def build_subscription_keyboard(channel_id: str, subscribe_text: str, check_text: str) -> InlineKeyboardMarkup:
    url = _channel_url(channel_id)
    buttons = [
        [InlineKeyboardButton(text=subscribe_text, url=url)],
        [InlineKeyboardButton(text=check_text, callback_data=CHECK_CALLBACK_DATA)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _channel_url(channel_id: str) -> str:
    clean_id = channel_id.strip()
    if clean_id.startswith("@"):
        clean_id = clean_id[1:]
    return f"https://t.me/{quote(clean_id)}"
