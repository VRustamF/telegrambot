import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config.config import Config, load_config
from handlers import others, users

logger = logging.getLogger(__name__)

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запуск бота'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/stats',
                   description='Статистика пользователя')
    ]

    await bot.set_my_commands(main_menu_commands)

async def main():
    config: Config = load_config()

    logging.basicConfig(
        level=config.log.level,
        format=config.log.format,
    )

    logger.info("Starting bot")

    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.startup.register(set_main_menu)

    dp.include_router(users.router)
    dp.include_router(others.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())