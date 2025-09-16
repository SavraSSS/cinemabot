import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db import DB

API_TOKEN = ""

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher()

class FavMovie(StatesGroup):
    waiting_for_title = State()

#def repo(event) -> DB:
    #return event.dispatcher["db"]

@dp.message(Command(commands = ['start','Start']))
async def start_handler(message: types.Message, state: FSMContext):
    #await repo(message).upsert_user(
    #    user_id=message.from_user.id,
    #    username=message.from_user.username)
    await state.set_state(FavMovie.waiting_for_title)
    await message.answer('Привет! Напиши любимый фильм')

@dp.message(Command(commands = ['favorite_film', 'Favorite_film']))
async def fav_handler(message: types.Message, state: FSMContext):
    await state.set_state(FavMovie.waiting_for_title)
    await message.answer("Какой твой любимый фильм?")


@dp.message(Command(commands=['info','Info']))
async def info_handler(message: types.Message, state: FSMContext):
    await message.answer("""Основная цель существования бота - помочь с выбором фильмов и сериалов, подсказать на основе предпочтений пользователя\nРазработчик - SavraSSS\n2025
                         """)


@dp.message(FavMovie.waiting_for_title, F.text)
async def process_fav(message: types.Message, state: FSMContext):
    title = message.text.strip()
    if title[0] != '/':
        await message.answer(f"Запомнил твой любимый фильм: {title}")
    else:
        await message.answer(f"К сожалению это не фильм")
    await state.clear()


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