from aiogram.fsm.state import State, StatesGroup


class OnboardingStates(StatesGroup):
    start = State()
    ask_login = State()
    wait_email_code = State()
    check_channel = State()
    bonus_grant = State()
    done = State()
