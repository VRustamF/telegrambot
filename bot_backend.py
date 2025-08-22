from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message) -> None:
    await message.answer(text='Салам брат')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    await message.answer(text='Напиши мне что-нибудь и в ответ я пришлю тебе твое сообщение')


@dp.message()
async def send_echo(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается ')


if __name__ == '__main__':
    dp.run_polling(bot)