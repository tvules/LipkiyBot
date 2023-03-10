from enum import Enum


class CommonAnswer(str, Enum):
    """Answers for common handling."""

    GREETING = "👋🏻"


class StickerAnswer(str, Enum):
    """Answers for sticker handling."""

    STICKERSET_IS_FULL = (
        "К сожалению, мне не удалось создать новый стикер, "
        "потому что набор стикеров уже переполнен 🙄.\n\n"
        "Для удаления ненужных стикеров воспользуйся командой /delsticker."
    )
    STICKERSET_IS_EMPTY = "У Вас пока нет ни одного стикера."
    USER_NOT_OWNER_OF_STICKERSET = (
        "К сожалению, это действие невозможно, поскольку "
        "Вы не являетесь создателем соответствующего набора стикеров."
    )
    CHOOSE_STICKER = "Отправь мне стикер, который хочешь удалить."
    STICKER_SUCCESS_DELETED = (
        "Стикер успешно удален, "
        "в течение часа он пропадет из набора у всех пользователей."
    )
    STICKER_ALREADY_DELETED = "Этот стикер уже удален из набора стикеров."


class StickerConst(str, Enum):
    """Default sticker constants."""

    STICKER_EMOJI = "🤖"
