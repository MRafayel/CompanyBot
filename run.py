import asyncio
import sys
import logging

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from Bot.handlers import router
from aiogram.client.default import DefaultBotProperties
from config import TOKEN
from DB.database import create_db


async def main():
    create_db()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Exit")
