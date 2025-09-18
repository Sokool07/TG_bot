from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.i18n import gettext as _

from bot.core.config import settings

router = Router(name="notcoin")


def _notcoin_keyboard() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(
        text=_("notcoin button"),
        web_app=WebAppInfo(url=settings.NOTCOIN_APP_URL),
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


@router.message(Command(commands=["notcoin", "coin"]))
async def handle_notcoin(message: types.Message) -> None:
    await message.answer(_("notcoin description"), reply_markup=_notcoin_keyboard())
