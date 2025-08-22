from tkinter.font import names

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from random import randint
from dataclasses import dataclass

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()

ATTEMPTS = 6

users = {}


@dataclass
class User:
    game: str | None = None
    number: int | None = None
    attempts: int | None = None
    total_games: int = 0
    wins: int = 0


def get_random_numb() -> int:
    return randint(1, 100)


def guess_number_game(message: Message) -> bool:
    user = message.from_user.id
    game = users[user].game
    return True if game == 'guess_number' else False


def echo_game(message: Message) -> bool:
    user = message.from_user.id
    game = users[user].game
    return True if game == 'echo' else False



@dp.message(CommandStart())
async def process_start_command(message: Message) -> None:
    await message.answer(text=f'Салам, {message.chat.username}. Го поиграем короче.\n\n'
                                'Угадай цифру: /guess_number\n'
                                'Повторялка: /echo')

    if message.from_user.id not in users:
        users[message.from_user.id] = User()


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    await message.answer(text=f'Я игровой бот, но пока только знаю две игры :(\n\n'
                              'Угадай цифру: /guess_number\n'
                              'Повторялка: /echo\n\n'
                              'Другие команды:\n'
                              'Узнать статистику: /stats')


@dp.message(Command(commands=['echo']))
async def process_echo_command(message: Message) -> None:
    user = message.from_user.id
    users[user].game = 'echo'
    await message.answer(text='Включена игра "Повторялка"!\n\n'
                              'Бот будет повторять за вами сообщения.\n\n'
                              'Чтобы выйти из игры воспользуйтесь командой /cancel')



@dp.message(Command(commands=['guess_number']))
async def process_guess_number_command(message: Message) -> None:
    user = message.from_user.id
    users[user].game = 'guess_number'
    users[user].number = get_random_numb()
    users[user].attempts = ATTEMPTS
    await message.answer(text='Включена игра "Угадай число"!\n\n'
                              'Бот придумает число от 1 до 100, ваша задача отгадать его за 6 шагов.\n\n'
                              'Чтобы выйти из игры воспользуйтесь командой /cancel')


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message) -> None:
    user = message.from_user.id
    if users[user].game == 'guess_number':
        users[user].game = None
        users[user].number = None
        users[user].attempts = None
        await message.answer(text='Вы успешно вышли из игры!')
    elif users[user].game == 'echo':
        users[user].game = None
        await message.answer(text='Вы успешно вышли из игры!')
    else:
        await message.answer(text='Игра не была запущена!')


@dp.message(Command(commands=['stats']))
async def process_stats_command(message: Message) -> None:
    user = message.from_user.id
    await message.answer(text=f'Ваша статистика:\n\nВсего игр: {users[user].total_games}\nПобед: {users[user].wins}')


@dp.message(guess_number_game)
async def process_guess_number_answer(message: Message) -> None:
    user = message.from_user.id
    secret_number = users[user].number
    print(secret_number)

    numb = message.text

    if numb.isdigit() and 1 <= int(numb) <= 100:
        numb = int(numb)

        if numb == secret_number:
            users[user].game = None
            users[user].number = None
            users[user].attempts = None
            users[user].total_games += 1
            users[user].wins += 1
            await message.answer(text='Молодец чемпион, ты победил!!!')

        elif numb > secret_number:
            users[user].attempts -= 1
            if users[user].attempts > 0:
                await message.answer(text='Моё число меньше! Попробуй ещё раз лошпед. Можешь сдаться командой /cancel\n\n'
                                         f'Осталось попыток: {users[user].attempts}')
        elif numb < secret_number:
            users[user].attempts -= 1
            if users[user].attempts > 0:
                await message.answer(text='Моё число больше! Попробуй ещё раз лошпед. Можешь сдаться командой /cancel\n\n'
                                         f'Осталось попыток: {users[user].attempts}')

        if users[user].attempts == 0:
            users[user].game = None
            users[user].number = None
            users[user].attempts = None
            users[user].total_games += 1
            await message.answer(text='Боже проиграл лох ботик фууууу')


@dp.message(echo_game)
async def process_echo_answer(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается ')


@dp.message()
async def process_answer(message: Message) -> None:
    await message.answer(text='К сожалению ты не начал игру.\n\nУзнай как начать игру с помощью команты /help')


if __name__ == '__main__':
    dp.run_polling(bot)