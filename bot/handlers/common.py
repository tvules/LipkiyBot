from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.constants import CommonMessage

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """Handler of the /start command."""

    await message.answer(
        text=CommonMessage.GREETING.format(username=message.from_user.username)
    )
