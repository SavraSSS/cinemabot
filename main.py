import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = ""

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands = ['start','Start']))
async def start_handler(message: types.Message):
    await message.answer('Привет! Напиши любимый фильм')

@dp.message()
async def update_handler(message: types.Message):
    await message.answer('Снова здарова')


async def main():
    async with bot:
        await bot.delete_webhook(drop_pending_updates=True)
        me = await bot.get_me()
        logging.info(f"Bot started as @{me.username}")
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())