import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.config import settings
from bot.handlers import main_router


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)

    await dp.start_polling(
        Bot(settings.TOKEN, parse_mode=ParseMode.HTML),
    )


asyncio.run(main())
