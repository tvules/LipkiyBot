import re

from aiogram import Bot, F, Router
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message

from bot.constants import (
    MessageStickerAnswer,
    MessageStickerConst,
    MessageStickerErrorAnswer,
)
from bot.schemas import MessageAuthor, MessageStickerCreate
from bot.services import (
    create_message_sticker_image,
    get_stickerset_name_by_user,
)
from bot.states import DeleteStickerState
from bot.utils import download_user_avatar

router = Router()


@router.message(F.text, F.forward_from)
async def create_sticker_from_handler(message: Message, bot: Bot) -> None:
    """Create a sticker from message forwarded from a user."""

    return await create_sticker_callback(
        message,
        bot,
        MessageStickerCreate(
            author=MessageAuthor(
                first_name=message.forward_from.first_name,
                last_name=message.forward_from.last_name,
                avatar=await download_user_avatar(bot, message.forward_from),
            ),
            text=message.text,
        ),
    )


@router.message(F.text, F.forward_from_chat)
async def create_sticker_from_chat_handler(message: Message, bot: Bot) -> None:
    """Create a sticker from message forwarded from chat."""

    avatar = None
    if photo := (await bot.get_chat(message.forward_from_chat.id)).photo:
        avatar = await bot.download(photo.small_file_id)

    return await create_sticker_callback(
        message,
        bot,
        MessageStickerCreate(
            author=MessageAuthor(
                first_name=message.forward_from_chat.title,
                avatar=avatar,
            ),
            text=message.text,
        ),
    )


@router.message(F.text, F.forward_sender_name)
async def create_sticker_from_sender_handler(
    message: Message, bot: Bot
) -> None:
    """Create a sticker from message forwarded from a private user."""

    return await create_sticker_callback(
        message,
        bot,
        MessageStickerCreate(
            author=MessageAuthor(first_name=message.forward_sender_name),
            text=message.text,
        ),
    )


async def create_sticker_callback(
    message: Message, bot: Bot, sticker_create: MessageStickerCreate
) -> None:
    """Create a sticker."""

    await bot.send_chat_action(message.from_user.id, ChatAction.CHOOSE_STICKER)

    set_name = await get_stickerset_name_by_user(message.from_user, bot)
    sticker = create_message_sticker_image(sticker_create)
    input_png = BufferedInputFile(sticker.read(), "message_sticker.png")

    try:
        await bot.add_sticker_to_set(
            message.from_user.id,
            set_name,
            MessageStickerConst.STICKER_EMOJI,
            input_png,
        )
    except TelegramBadRequest as exc:
        if re.search(r"STICKERSET_INVALID", exc.message, re.I):
            await bot.create_new_sticker_set(
                message.from_user.id,
                set_name,
                f"Created by @{(await bot.me()).username}",
                MessageStickerConst.STICKER_EMOJI,
                input_png,
            )

        elif re.search(r"STICKERPACK_STICKERS_TOO_MUCH", exc.message, re.I):
            await message.answer(
                MessageStickerErrorAnswer.STICKERPACK_STICKERS_TOO_MUCH
            )
            return

        elif re.search(r"STICKER_PNG_DIMENSIONS", exc.message, re.I):
            await message.reply(
                MessageStickerErrorAnswer.STICKER_PNG_DIMENSIONS
            )
            return

        else:
            raise

    set_ = await bot.get_sticker_set(set_name)
    await message.reply_sticker(set_.stickers[-1].file_id)


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
            await message.answer(MessageStickerErrorAnswer.STICKERSET_IS_EMPTY)
            return

        else:
            raise

    await state.set_state(DeleteStickerState.choose_sticker)
    await message.answer(MessageStickerAnswer.CHOOSE_STICKER)


@router.message(DeleteStickerState.choose_sticker, F.sticker)
async def command_delsticker_state_choose_sticker_handler(
    message: Message, bot: Bot, state: FSMContext
) -> None:
    """Handler for the state "choose_sticker" of the /delsticker command."""

    if message.sticker.set_name != await get_stickerset_name_by_user(
        message.from_user, bot
    ):
        await message.reply(
            MessageStickerErrorAnswer.USER_NOT_OWNER_OF_STICKERSET
        )
        return

    try:
        await message.sticker.delete_from_set()
    except TelegramBadRequest as exc:
        if re.search(r"STICKERSET_NOT_MODIFIED", exc.message, re.I):
            await message.reply(
                MessageStickerErrorAnswer.STICKER_ALREADY_DELETED
            )
            return

        else:
            raise

    await state.clear()
    await message.answer(MessageStickerAnswer.STICKER_SUCCESS_DELETED)
