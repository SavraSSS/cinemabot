import asyncio
import logging
import random
import asyncpg
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from db import *

API_TOKEN = ""

err_phr = ['Упс... такой команды нет', 'Такой команды я пока не знаю, но обязательно узнаю!', 'Я не знаю эту команду']

rand_phr = ['Вот тебе случайный фильм на сегодня:', 'Посмотри вот это:', 'Рекомендую посмотреть', 'Рандом есть рандом, придется смотреть']
rand_mas = ['Остров проклятых', 'Престиж', 'Интерстеллар', 'Титаник', 'Хатико', 'Смешарики', 'Начало', 'Довод', 'Миссия невыполнима', 'Назад в будущее']

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Буду смотреть", callback_data="like_random_film"),
     InlineKeyboardButton(text="Не нравится", callback_data="dislike_random_film")],
])

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher()

class FavMovie(StatesGroup):
    waiting_for_title = State()

@dp.message(Command(commands = ['start','Start']))
async def start_handler(message: types.Message, state: FSMContext, pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        await conn.execute(UPDATE_USER, message.from_user.id, message.from_user.username)
    await state.set_state(FavMovie.waiting_for_title)
    await message.answer('Привет! Какой твой любимый фильм?')

@dp.message(Command(commands = ['set_film', 'Set_film']))
async def fav_handler(message: types.Message, state: FSMContext):
    await state.set_state(FavMovie.waiting_for_title)
    await message.answer("Какой твой любимый фильм?")

@dp.message(Command(commands=['favorite_film', 'Favorite_film']))
async def fav_handler(message: types.Message, pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(GET_FAVORITE, message.from_user.id)
    fav = row["favorite_movie"] if row and row["favorite_movie"] else None
    await message.answer(f"Твой любимый фильм: {fav}" if fav else "Ещё не задан")

@dp.message(Command(commands = ['random_film', 'Random_film']))
async def rand_handler(message: types.Message):
    await message.answer(random.choice(rand_phr) + ' ' + random.choice(rand_mas), reply_markup=ikb)
    

@dp.message(Command(commands=['info','Info']))
async def info_handler(message: types.Message):
    await message.answer("Основная цель существования бота - помочь с выбором фильмов и сериалов, подсказать на основе ваших предпочтений\nРазработчик - SavraSSS\n2025")

@dp.message(F.text.startswith("/"))
async def catch_any_command(message: types.Message):
    await message.answer(random.choice(err_phr))
    await message.answer(f"Попробуйте ввести другую команду вместо {message.text}")

@dp.message(FavMovie.waiting_for_title, F.text)
async def process_fav(message: types.Message, state: FSMContext, pool: asyncpg.Pool):
    title = message.text.strip()
    if title == 'Букины' or title == 'букины':
        await message.answer(f"ООО, {title} 10/10")
    elif title[0] != '/':
        async with pool.acquire() as conn:
            status = await conn.execute(SET_FAVORITE, message.from_user.id, title)
        print(status)
        await message.answer(f"Запомнил твой любимый фильм: {title}")
    else:
        await message.answer(f"К сожалению это не фильм")
    await state.clear()


@dp.message()
async def update_handler(message: types.Message):
    await message.answer('Здарова')


@dp.callback_query()
async def callbacks_handler(callback: types.CallbackQuery):
    if callback.data == "like_random_film":
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Отлично")
    elif callback.data == "dislike_random_film":
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Жаль, попробуй еще раз")


async def main():
    pool = await asyncpg.create_pool('postgresql://bot:0109@localhost:5432/cinemabot', min_size=1, max_size=5)

    async with pool.acquire() as conn:
        await conn.execute(CREATE_USERS_SQL)

    dp["pool"] = pool
    async with bot:
        await bot.delete_webhook(drop_pending_updates=True)
        me = await bot.get_me()
        logging.info(f"Bot started as @{me.username}")
        try:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        finally:
            await pool.close()


if __name__ == "__main__":
    asyncio.run(main())