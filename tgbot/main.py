from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiohttp.web import run_app
from aiohttp.web_app import Application

from tgbot.config import settings
from tgbot.handlers import router


def get_bot():
    """Get a bot object."""

    return Bot(settings.token.get_secret_value())


def get_dispatcher() -> Dispatcher:
    """Get a dispatcher object."""

    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    return dispatcher


def get_application() -> Application:
    """Get an application object."""

    return Application()


async def _set_webhook(bot: Bot, webhook_url: str) -> None:
    """Set webhook for the bot on the telegram server."""

    await bot.set_webhook(webhook_url, drop_pending_updates=True)


async def _delete_webhook(bot: Bot) -> None:
    """Delete webhook for the bot from the telegram server."""

    await bot.delete_webhook()


def _start_webhook(
    dispatcher: Dispatcher, bot: Bot, *, prefix: str, host: str, port: int
) -> None:
    """Start the application in the "webhook" mode."""

    app = get_application()

    SimpleRequestHandler(
        dispatcher,
        bot,
    ).register(app, path=prefix)
    setup_application(app, dispatcher, bot=bot)

    run_app(app, host=host, port=port)


def start_webhook(
    dispatcher: Dispatcher,
    bot: Bot,
    *,
    prefix: str = "/",
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    """Start the application in the "webhook" mode."""

    dispatcher.startup.register(_set_webhook)
    dispatcher.shutdown.register(_delete_webhook)

    _start_webhook(dispatcher, bot, prefix=prefix, host=host, port=port)


def start_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    """Start the application in the "long-polling" mode."""

    dispatcher.run_polling(bot)


def run():
    """Start the bot."""

    bot = get_bot()
    dispatcher = get_dispatcher()

    if settings.webhook_host:
        dispatcher["webhook_url"] = (
            settings.webhook_host + settings.webhook_prefix
        )
        start_webhook(
            dispatcher,
            bot,
            prefix=settings.webhook_prefix,
            host=settings.host,
            port=settings.port,
        )
    else:
        start_polling(dispatcher, bot)
