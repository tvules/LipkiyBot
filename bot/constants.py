from enum import Enum


class CommonAnswer(str, Enum):
    """Answers for common handling."""

    GREETING = "👋🏻"
    UNCAUGHT_ERROR = "Что-то произошло не так..."


class StickerAnswer(str, Enum):
    """Answers for sticker handling."""

    STICKERSET_IS_EMPTY = "У Вас пока нет ни одного стикера."
    USER_NOT_OWNER_OF_STICKERSET = (
        "К сожалению, это действие невозможно, поскольку "
        "соответствующий набор стикеров создан не мной или "
        "Вы не являетесь его создателем."
    )
    CHOOSE_STICKER = "Отправь мне стикер, который хочешь удалить."
    STICKER_SUCCESS_DELETED = (
        "Стикер успешно удален, "
        "в течение часа он пропадет из набора у всех пользователей."
    )
    STICKER_ALREADY_DELETED = "Этот стикер уже удален из набора стикеров."


class MessageStickerErrorAnswer(str, Enum):
    """Answers for caught errors."""

    STICKERPACK_STICKERS_TOO_MUCH = (
        "Набор стикеров переполнен.\n\n"
        "Команда /delsticker, для удаления ненужных стикеров."
    )
    STICKER_PNG_DIMENSIONS = (
        "Текст сообщения не помещается в допустимые размеры стикера."
    )


class MessageStickerConst(str, Enum):
    """Message sticker constants."""

    STICKER_EMOJI = "💬"
