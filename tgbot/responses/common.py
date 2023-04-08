from enum import Enum


class CmdStartAnswer(str, Enum):
    """Messages to respond to the /start command."""

    GREETING = "👋🏻"


class CmdCancelAnswer(str, Enum):
    """Messages to respond to the /cancel command."""

    SUCCESS = "Все активные команды отменены."
    NO_ACTIVE_COMMANDS = "Нет активных команд, чтобы их отменять."


class UncaughtErrorsAnswer(str, Enum):
    """Messages to respond to the uncaught error handler."""

    UNCAUGHT = "Что-то произошло не так..."
