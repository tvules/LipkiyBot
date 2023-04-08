from enum import Enum


class CreateStickerAnswer(str, Enum):
    """Messages to respond to the creation sticker handler."""

    STICKERPACK_STICKERS_TOO_MUCH = (
        "Набор стикеров переполнен.\n\n"
        "Команда /delsticker, для удаления ненужных стикеров."
    )
    STICKER_PNG_DIMENSIONS = (
        "Текст сообщения не помещается в допустимые размеры стикера."
    )


class CmdDelstickerAnswer(str, Enum):
    """Messages to respond to the /delsticker command."""

    CHOOSE_STICKER = "Отправьте стикер, который хотите удалить."
    STICKERSET_IS_EMPTY = "У Вас пока нет созданных стикеров."
    USER_NOT_OWNER_OF_STICKERSET = (
        "Этот стикер создан не мной или Вы не являетесь его владельцем."
    )
    STICKER_ALREADY_DELETED = "Этот стикер уже удален из набора."
    STICKER_SUCCESS_DELETED = (
        "Стикер успешно удален, "
        "в течение часа он пропадет из набора у всех пользователей."
    )