from aiogram import Router
from aiogram.types import ErrorEvent

from bot.constants import CommonAnswer

router = Router()


@router.errors()
async def uncaught_error_handler(exception: ErrorEvent) -> None:
    """Handler for uncaught errors."""

    await exception.update.message.answer(CommonAnswer.UNCAUGHT_ERROR)
