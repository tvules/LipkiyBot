from aiogram import Router

from . import common, message_sticker

router = Router()

router.include_routers(
    common.router,
    message_sticker.router,
)
