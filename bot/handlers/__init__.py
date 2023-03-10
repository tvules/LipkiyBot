from aiogram import Router

from .common import router as common_router
from .error import router as error_router
from .message_sticker import router as sticker_router

__all__ = (
    "main_router",
    "common_router",
    "sticker_router",
    "error_router",
)

main_router = Router()

main_router.include_routers(
    common_router,
    sticker_router,
    error_router,
)
