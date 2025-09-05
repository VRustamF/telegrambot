from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON



def create_bookmarks_buttons(bookmarks: set, delete: str | None = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    bookmarks_button: list[InlineKeyboardButton] = []

    for bookmark in bookmarks:
        bookmarks_button.append(
            InlineKeyboardButton(text=LEXICON['del'] + bookmark if delete else bookmark, callback_data=bookmark[0] + delete if delete else bookmark[0] + 'page')
        )

    if delete:
        buttons: list[InlineKeyboardButton] = [
            InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel')
        ]
    else:
        buttons: list[InlineKeyboardButton] = [
            InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'], callback_data='del'),
            InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel')
        ]

    kb.row(*bookmarks_button, width=1)
    kb.row(*buttons, width=2)

    return kb.as_markup()
