import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from handlers import others, users

async def main() -> None:
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )

    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    dp.include_router(users.router)
    dp.include_router(others.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())