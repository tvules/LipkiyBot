from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants import CommonAnswer

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """Handler of the /start command."""

    await message.answer(
        text=CommonAnswer.GREETING.format(username=message.from_user.username)
    )


@router.message(Command("cancel"))
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    """Handler of the /cancel command."""

    if not await state.get_state():
        await message.answer(CommonAnswer.NO_ACTIVE_COMMANDS)
        return None

    await state.clear()
    await message.answer(CommonAnswer.SUCCESS_CANCELED)
