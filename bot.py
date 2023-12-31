import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import config
from handlers import start_handler, price_handler

bot = Bot(config.bot_token.get_secret_value())
dp = Dispatcher()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp.include_router(start_handler.router)
    dp.include_router(price_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())