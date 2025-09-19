from __future__ import annotations
import time
from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.utils.i18n import gettext as _

from bot.core.config import settings
from bot.keyboards.inline.menu import main_keyboard
from bot.keyboards.inline.onboarding import CHECK_CALLBACK_DATA, build_subscription_keyboard
from bot.services.analytics import analytics
from bot.services.onboarding import BonusGrantResult, confirm_token, grant_bonus, start_linking
from bot.states.onboarding import OnboardingStates

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

router = Router(name="onboarding")
THROTTLE_SECONDS = 10
MIN_IDENTIFIER_LENGTH = 3
MIN_TOKEN_LENGTH = 3
MIN_NAME_LENGTH_FOR_MASKING = 2


@router.message(CommandStart())
@analytics.track_event("Sign Up")
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(OnboardingStates.start)

    await message.answer(_("onboarding_welcome"))
    await message.answer(_("onboarding_ask_login"))
    await state.set_state(OnboardingStates.ask_login)


@router.message(Command("cancel"))
async def handle_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_("onboarding_cancelled"))


@router.message(OnboardingStates.ask_login, F.text)
async def process_login(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        return
        
    identifier = (message.text or "").strip()

    if len(identifier) < MIN_IDENTIFIER_LENGTH:
        await message.answer(_("onboarding_invalid_login"))
        return

    try:
        result = await start_linking(message.from_user.id, identifier)
    except NotImplementedError:
        await message.answer(_("onboarding_service_error"))
        return
    except Exception:  # noqa: BLE001
        await message.answer(_("onboarding_service_error"))
        return

    await state.update_data(
        telegram_id=message.from_user.id,
        login=identifier,
        email=result.email,
        casino_user_id=result.casino_user_id,
        last_check=0.0,
    )

    masked_email = _mask_email(result.email)
    await message.answer(
        _("onboarding_code_sent").format(email=masked_email, ttl=settings.EMAIL_TOKEN_TTL_MINUTES),
    )
    await message.answer(_("onboarding_ask_code"))
    await state.set_state(OnboardingStates.wait_email_code)


@router.message(OnboardingStates.wait_email_code, F.text)
async def process_token(message: Message, state: FSMContext) -> None:
    if not message.from_user:
        return
        
    token = (message.text or "").strip()

    if len(token) < MIN_TOKEN_LENGTH:
        await message.answer(_("onboarding_token_invalid"))
        return

    try:
        casino_user_id = await confirm_token(message.from_user.id, token)
    except NotImplementedError:
        await message.answer(_("onboarding_service_error"))
        return
    except Exception:  # noqa: BLE001
        await message.answer(_("onboarding_token_invalid"))
        return

    await state.update_data(casino_user_id=casino_user_id)

    keyboard = build_subscription_keyboard(
        channel_id=settings.CHANNEL_ID,
        subscribe_text=_("onboarding_subscribe_button"),
        check_text=_("onboarding_check_button"),
    )

    await message.answer(_("onboarding_token_confirmed"))
    await message.answer(_("onboarding_subscribe_prompt"), reply_markup=keyboard)
    await state.set_state(OnboardingStates.check_channel)


@router.callback_query(OnboardingStates.check_channel, F.data == CHECK_CALLBACK_DATA)
async def process_check_subscription(callback: CallbackQuery, state: FSMContext) -> None:
    if not callback.message or not callback.from_user:
        return
        
    await callback.answer()

    data = await state.get_data()
    now = time.monotonic()
    last_check = float(data.get("last_check", 0.0))

    if last_check and (elapsed := now - last_check) < THROTTLE_SECONDS:
        remaining = int(THROTTLE_SECONDS - elapsed) or 1
        await callback.message.answer(_("onboarding_throttled").format(seconds=remaining))
        return

    await state.update_data(last_check=now)

    if not await _is_member(callback, callback.from_user.id):
        await callback.message.answer(_("onboarding_not_subscribed"))
        return

    await callback.message.answer(_("onboarding_granting"))

    casino_user_id = data.get("casino_user_id")
    if not casino_user_id:
        await callback.message.answer(_("onboarding_token_invalid"))
        return

    await state.set_state(OnboardingStates.bonus_grant)

    try:
        result = await grant_bonus(callback.from_user.id, str(casino_user_id))
    except NotImplementedError:
        await callback.message.answer(_("onboarding_service_error"))
        await state.clear()
        return
    except Exception:  # noqa: BLE001
        result = BonusGrantResult(success=False)

    if result.success:
        await callback.message.answer(_("onboarding_bonus_success"))
        await callback.message.answer(_("title main keyboard"), reply_markup=main_keyboard())
    else:
        message_key = (
            "onboarding_requirements_failed" if result.reason == "requirements" else "onboarding_bonus_failure"
        )
        await callback.message.answer(_(message_key))

    await state.set_state(OnboardingStates.done)
    await state.clear()


def _mask_email(email: str) -> str:
    if "@" not in email:
        return email
    name, domain = email.split("@", 1)
    masked = name[0] + "*" if len(name) <= MIN_NAME_LENGTH_FOR_MASKING else name[0] + "*" * (len(name) - 2) + name[-1]
    return f"{masked}@{domain}"


async def _is_member(callback: CallbackQuery, user_id: int) -> bool:
    if settings.INTEGRATIONS_STUB:
        return True

    if not callback.message or not callback.message.bot:
        return False

    try:
        member = await callback.message.bot.get_chat_member(settings.CHANNEL_ID, user_id)
    except TelegramBadRequest:
        return False

    return getattr(member, "status", None) in {"member", "administrator", "creator"}
