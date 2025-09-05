import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import Config, load_config
from keyboards.menu_commands import set_main_menu
from handlers import others, users
from services.file_handling import prepare_book
from database.database import init_db



logger = logging.getLogger(__name__)

async def main() -> None:
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )

    logger.info('Bot starting...')

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    logger.info('Подготовка книги...')
    book = prepare_book('book/book.txt')
    logger.info(f'Книга готова! Количество страниц: {len(book)}')

    db: dict = init_db()

    dp.workflow_data.update(book=book, db=db)

    await set_main_menu(bot=bot)

    dp.include_router(router=users.router)
    dp.include_router(router=others.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())