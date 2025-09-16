import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db import DB

API_TOKEN = ""

err_phr = ['Упс... такой команды нет', 'Такой команды я пока не знаю, но обязательно узнаю!', 'Я не знаю эту команду']

rand_phr = ['Вот тебе случайный фильм на сегодня:', 'Посмотри вот это:', 'Рекомендую посмотреть', 'Рандом есть рандом, придется смотреть']
rand_mas = ['Остров проклятых', 'Престиж', 'Интерстеллар', 'Титаник', 'Хатико', 'Смешарики', 'Начало', 'Довод', 'Миссия невыполнима', 'Назад в будущее']

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
    await message.answer('Привет! Какой твой любимый фильм?')

@dp.message(Command(commands = ['favorite_film', 'Favorite_film']))
async def fav_handler(message: types.Message, state: FSMContext):
    await state.set_state(FavMovie.waiting_for_title)
    await message.answer("Какой твой любимый фильм?")

@dp.message(Command(commands = ['random_film', 'Random_film']))
async def rand_handler(message: types.Message, state: FSMContext):
    await message.answer(random.choice(rand_phr) + ' ' + random.choice(rand_mas))

@dp.message(Command(commands=['info','Info']))
async def info_handler(message: types.Message, state: FSMContext):
    await message.answer("Основная цель существования бота - помочь с выбором фильмов и сериалов, подсказать на основе ваших предпочтений\nРазработчик - SavraSSS\n2025")

@dp.message(F.text.startswith("/"))
async def catch_any_command(message: types.Message):
    await message.answer(random.choice(err_phr))
    await message.answer(f"Попробуйте ввести другую команду вместо {message.text}")

@dp.message(FavMovie.waiting_for_title, F.text)
async def process_fav(message: types.Message, state: FSMContext):
    title = message.text.strip()
    if title == 'Букины' or title == 'букины':
        await message.answer(f"ООО, {title} 10/10")
    elif title[0] != '/':
        await message.answer(f"Запомнил твой любимый фильм: {title}")
    else:
        await message.answer(f"К сожалению это не фильм")
    await state.clear()


@dp.message()
async def update_handler(message: types.Message):
    await message.answer('Здарова')


async def main():
    async with bot:
        await bot.delete_webhook(drop_pending_updates=True)
        me = await bot.get_me()
        logging.info(f"Bot started as @{me.username}")
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())