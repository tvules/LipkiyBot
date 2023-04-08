from aiogram import Router

from . import cmd_start, cmd_cancel, uncaught_errors

router = Router()

router.include_routers(
    cmd_start.router,
    cmd_cancel.router,
    uncaught_errors.router
)
