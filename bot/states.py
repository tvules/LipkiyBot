from aiogram.fsm.state import State, StatesGroup


class DeleteStickerState(StatesGroup):
    choose_sticker = State()
