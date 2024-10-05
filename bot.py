import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from conf import ADMIN, TOKEN
import database

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def start_bot():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start_command(message: Message):
    database.check_user(message.from_user.username)
    await message.answer("ok")