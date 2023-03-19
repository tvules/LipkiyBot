from enum import Enum


class CommonAnswer(str, Enum):
    """Answers for common handling."""

    GREETING = "👋🏻"
    UNCAUGHT_ERROR = "Что-то произошло не так..."
    SUCCESS_CANCELED = "Все активные команды отменены."
    NO_ACTIVE_COMMANDS = "Нет активных команд, чтобы их отменять."


class MessageStickerAnswer(str, Enum):
    """Answers for message sticker handling."""

    CHOOSE_STICKER = "Отправьте стикер, который хотите удалить."
    STICKER_SUCCESS_DELETED = (
        "Стикер успешно удален, "
        "в течение часа он пропадет из набора у всех пользователей."
    )


class MessageStickerErrorAnswer(str, Enum):
    """Answers for caught errors."""

    STICKERPACK_STICKERS_TOO_MUCH = (
        "Набор стикеров переполнен.\n\n"
        "Команда /delsticker, для удаления ненужных стикеров."
    )
    STICKER_PNG_DIMENSIONS = (
        "Текст сообщения не помещается в допустимые размеры стикера."
    )
    STICKERSET_IS_EMPTY = "У Вас пока нет созданных стикеров."
    USER_NOT_OWNER_OF_STICKERSET = (
        "Этот стикер создан не мной или Вы не являетесь его владельцем."
    )
    STICKER_ALREADY_DELETED = "Этот стикер уже удален из набора."


class MessageStickerConst(str, Enum):
    """Message sticker constants."""

    STICKER_EMOJI = "💬"
