from enum import Enum


class CommonAnswer(str, Enum):
    """Answers for common handling."""

    GREETING = "👋🏻"


class StickerAnswer(str, Enum):
    """Answers for sticker handling."""

    STICKER_SET_IS_FULL = (
        "К сожалению, мне не удалось создать новый стикер, "
        "потому что набор стикеров уже переполнен 🙄.\n\n"
        "Удалить старые стикеры можешь через @Stickers."
    )


class StickerConst(str, Enum):
    """Default sticker constants."""

    STICKER_EMOJI = "🤖"
