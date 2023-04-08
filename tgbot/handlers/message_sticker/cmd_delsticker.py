import re

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.responses.message_sticker import CmdDelstickerAnswer
from tgbot.services import get_stickerset_name_by_user
from tgbot.states.message_sticker import CmdDelStickerState

router = Router()


@router.message(Command("delsticker"), ~F.forward_from)
async def command_delsticker_handler(
    message: Message, bot: Bot, state: FSMContext
) -> None:
    """Handler of the /delsticker command."""

    try:
        await bot.get_sticker_set(
            await get_stickerset_name_by_user(message.from_user, bot)
        )
    except TelegramBadRequest as exc:
        if re.search(r"STICKERSET_INVALID", exc.message, re.I):
            await message.answer(CmdDelstickerAnswer.STICKERSET_IS_EMPTY)
            return

        else:
            raise

    await state.set_state(CmdDelStickerState.choose_sticker)
    await message.answer(CmdDelstickerAnswer.CHOOSE_STICKER)


@router.message(CmdDelStickerState.choose_sticker, F.sticker)
async def command_delsticker_state_choose_sticker_handler(
    message: Message, bot: Bot, state: FSMContext
) -> None:
    """Handler for the state "choose_sticker" of the /delsticker command."""

    if message.sticker.set_name != await get_stickerset_name_by_user(
        message.from_user, bot
    ):
        await message.reply(
            CmdDelstickerAnswer.USER_NOT_OWNER_OF_STICKERSET
        )
        return

    try:
        await message.sticker.delete_from_set()
    except TelegramBadRequest as exc:
        if re.search(r"STICKERSET_NOT_MODIFIED", exc.message, re.I):
            await message.reply(
                CmdDelstickerAnswer.STICKER_ALREADY_DELETED
            )
            return

        else:
            raise

    await state.clear()
    await message.answer(CmdDelstickerAnswer.STICKER_SUCCESS_DELETED)
