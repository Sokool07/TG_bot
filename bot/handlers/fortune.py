from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.core.config import settings

router = Router(name="fortune")


def _fortune_keyboard() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text=_("fortune button"), url=settings.FORTUNE_APP_URL)
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


@router.message(Command(commands=["fortune", "wheel", "game"]))
async def handle_fortune(message: types.Message) -> None:
    await message.answer(_("fortune description"), reply_markup=_fortune_keyboard())
