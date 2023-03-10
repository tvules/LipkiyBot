import re

from aiogram import Bot, F, Router
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, Message, User

from bot.constants import StickerAnswer, StickerConst
from bot.services import create_sticker_image
from bot.utils import create_uuid_from_user_id

router = Router()


@router.message(F.forward_from & F.text)
async def create_sticker_handler(message: Message) -> None:
    """Create a sticker from the forwarded message."""

    bot: Bot = Bot.get_current()
    bot_info: User = await bot.me()

    await bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.CHOOSE_STICKER
    )

    set_id = create_uuid_from_user_id(user_id=message.from_user.id)
    set_name = f"Set_{set_id}_by_{bot_info.username}"
    sticker = await create_sticker_image(
        bot=bot, author=message.forward_from, text=message.text
    )
    input_png = BufferedInputFile(
        file=sticker.read(), filename="message_sticker.png"
    )

    try:
        await bot.add_sticker_to_set(
            user_id=message.from_user.id,
            name=set_name,
            emojis=StickerConst.STICKER_EMOJI,
            png_sticker=input_png,
        )
    except TelegramBadRequest as exc:
        if re.search(r"STICKERPACK_STICKERS_TOO_MUCH", exc.message):
            await message.reply(StickerAnswer.STICKER_SET_IS_FULL)
            return

        elif re.search(r"STICKERSET_INVALID", exc.message):
            await bot.create_new_sticker_set(
                user_id=message.from_user.id,
                name=set_name,
                title="Message Stickers",
                emojis=StickerConst.STICKER_EMOJI,
                png_sticker=input_png,
            )

        else:
            raise

    set_ = await bot.get_sticker_set(set_name)
    await message.reply_sticker(set_.stickers[-1].file_id)
