from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.constants import CommonAnswer

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """Handler of the /start command."""

    await message.answer(
        text=CommonAnswer.GREETING.format(username=message.from_user.username)
    )
