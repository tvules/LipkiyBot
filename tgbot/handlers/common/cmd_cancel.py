from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.responses.common import CmdCancelAnswer

router = Router()


@router.message(Command("cancel"))
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    """Handler of the /cancel command."""

    if not await state.get_state():
        await message.answer(CmdCancelAnswer.NO_ACTIVE_COMMANDS)
        return None

    await state.clear()
    await message.answer(CmdCancelAnswer.SUCCESS)
