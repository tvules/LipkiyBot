from aiogram.fsm.state import State, StatesGroup


class CmdDelStickerState(StatesGroup):
    choose_sticker = State()