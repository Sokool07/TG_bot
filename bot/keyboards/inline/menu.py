from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.config import settings


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text=_("info button"), callback_data="info")],
        [
            InlineKeyboardButton(
                text=_("fortune button"),
                web_app=WebAppInfo(url=settings.FORTUNE_APP_URL),
            )
        ],
        [
            InlineKeyboardButton(
                text=_("notcoin button"),
                web_app=WebAppInfo(url=settings.NOTCOIN_APP_URL),
            )
        ],
        [InlineKeyboardButton(text=_("support button"), callback_data="support")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1)

    return keyboard.as_markup()
