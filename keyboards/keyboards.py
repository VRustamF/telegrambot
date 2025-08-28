from aiogram.types import (
    KeyboardButton
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU


def create_keyboard(buttons: list[KeyboardButton]) -> ReplyKeyboardBuilder:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.row(*buttons)
    return menu_builder


yes_no_buttons = [KeyboardButton(text=el) for el in [LEXICON_RU['yes_button'], LEXICON_RU['no_button']]]
yes_no_keyboard = create_keyboard(yes_no_buttons).as_markup(resize_keyboard=True, one_time_keyboard=True,)

game_buttons = [KeyboardButton(text=el) for el in [LEXICON_RU['scissors'], LEXICON_RU['rock'], LEXICON_RU['paper']]]
game_keyboard = create_keyboard(game_buttons).as_markup(resize_keyboard=True)

