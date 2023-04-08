from aiogram import Router
from aiogram.types import ErrorEvent

from tgbot.responses.common import UncaughtErrorsAnswer

router = Router()


# @router.errors()
# async def uncaught_error_handler(exception: ErrorEvent) -> None:
#     """Handler for uncaught errors."""
#
#     await exception.update.message.answer(UncaughtErrorsAnswer.UNCAUGHT)
