from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON



def create_inline_kb(current: int, total: int, width: int = 3) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=LEXICON['backward'], callback_data='backward'),
        InlineKeyboardButton(text=f'{current}/{total}', callback_data=str(current)),
        InlineKeyboardButton(text=LEXICON['forward'], callback_data='forward')
    ]

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()