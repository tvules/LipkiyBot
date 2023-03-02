import asyncio

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.handlers import main_router


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)

    bot = Bot(settings.TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
