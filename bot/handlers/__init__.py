from aiogram import Router

from . import export_users, fortune, info, menu, notcoin, onboarding, support


def get_handlers_router() -> Router:
    router = Router()
    router.include_router(onboarding.router)
    router.include_router(info.router)
    router.include_router(fortune.router)
    router.include_router(notcoin.router)
    router.include_router(support.router)
    router.include_router(menu.router)
    router.include_router(export_users.router)

    return router
