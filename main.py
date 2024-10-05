import asyncio
from fastapi import FastAPI, Request
import uvicorn
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, Update

from conf import ADMIN, TOKEN
import database

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    database.check_user(message.from_user.username)
    await message.answer("ok")


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    url_webhook = '147.45.254.214/webhook'
    await bot.set_webhook(url=url_webhook,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    yield
    await bot.delete_webhook()

@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)



@app.get("/bot")
async def send_bot():
    await bot.send_message(ADMIN, "request to server detected")
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host="147.45.254.214", port=8042)