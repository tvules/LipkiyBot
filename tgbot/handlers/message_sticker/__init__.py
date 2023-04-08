from aiogram import Router

from . import cmd_delsticker, create_sticker

router = Router()

router.include_routers(
    cmd_delsticker.router,
    create_sticker.router,
)
