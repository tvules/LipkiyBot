from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgbot.responses.common import CmdStartAnswer

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handler of the /start command."""

    await message.answer(
        text=CmdStartAnswer.GREETING.format(
            username=message.from_user.username
        )
    )
