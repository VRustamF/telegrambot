from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import yes_no_keyboard, game_keyboard

from services.creating_users import add_user, USERS
from services.services import choose_a_winner, make_a_choice

router = Router()

@router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_keyboard)

    if message.from_user.id not in USERS:
        await add_user(message.from_user.id)


@router.message(Command(commands='stats'))
async def process_command_stats(message: Message):
    await message.reply(text=f'Всего игр: {USERS[message.from_user.id].total_games}\nПобед: {USERS[message.from_user.id].wins}')


@router.message(Command(commands='help'))
async def process_command_help(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_keyboard)


@router.message(F.text == LEXICON_RU['yes_button'])
async def process_go(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_keyboard)


@router.message(F.text == LEXICON_RU['no_button'])
async def process_no(message: Message):
    await message.answer(text=LEXICON_RU['no'])


@router.message(F.text.in_({LEXICON_RU['scissors'], LEXICON_RU['rock'], LEXICON_RU['paper']}))
async def process_choice(message: Message):
    bot_choice = make_a_choice()
    await message.answer(text=f'{LEXICON_RU['bot_choice']} - {bot_choice}')

    winner = choose_a_winner(message.text, bot_choice)
    if winner == LEXICON_RU['user_won']:
        USERS[message.from_user.id].total_games += 1
        USERS[message.from_user.id].wins += 1
        message_effect_id = '5046509860389126442'
    else:
        USERS[message.from_user.id].total_games += 1
        message_effect_id = None

    await message.answer(text=winner, message_effect_id=message_effect_id, reply_markup=yes_no_keyboard)