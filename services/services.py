from random import choice

from lexicon.lexicon import LEXICON_RU


def  make_a_choice() -> str:
    return choice([LEXICON_RU['scissors'], LEXICON_RU['rock'], LEXICON_RU['paper']])


def choose_a_winner(user_choice: str, bot_choice: str) -> str:
    rules = {'Ножницы ✂️': 'Бумага 📜', 'Камень 🗿': 'Ножницы ✂️', 'Бумага 📜':'Камень 🗿'}

    if bot_choice == user_choice:
        return LEXICON_RU['nobody_won']
    elif rules[user_choice] == bot_choice:
        return LEXICON_RU['user_won']
    else:
        return LEXICON_RU['bot_won']