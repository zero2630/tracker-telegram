import asyncio
import os
import datetime

import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel

from conf import TOKEN
import database
from database import check_user_confirmed


class SendMessage(BaseModel):
    ids: list[int]
    message: str

app = FastAPI()
BOT_TOKEN = TOKEN
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def check_deadlines(s, h):
    while True:
        if datetime.datetime.now().hour == h:
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            three_days = today + datetime.timedelta(days=3)

            deadlines = database.check_deadlines(today)
            deadlines1 = database.check_deadlines(tomorrow)
            deadlines3 = database.check_deadlines(three_days)

            for el in deadlines:
                await send_message(el[0], f"У тебя горит дедлайн по задаче \"{el[1]}\"")
            for el in deadlines1:
                await send_message(el[0], f"Завтра дедлайн по задаче \"{el[1]}\"")
            for el in deadlines3:
                await send_message(el[0], f"Через три дня дедлайн по задаче \"{el[1]}\"")
            await asyncio.sleep(s)

async def get_updates(offset=None):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/getUpdates", params={"offset": offset})
        return response.json()

async def send_message(chat_id, text):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

async def poll_updates():
    offset = None
    while True:
        updates = await get_updates(offset)
        for update in updates.get("result", []):
            chat_id = update["message"]["chat"]["id"]
            message_text = update["message"]["text"]
            username = update["message"]["chat"]["username"]
            if message_text == "/start":
                if not database.check_user(username):
                    database.set_confirmed_tg(username, chat_id)
                    await send_message(chat_id, f"Верификация прошла успешно, {username}")
                else:
                    await send_message(chat_id, f"Вы не зарегистрированы в сервисе")
            offset = update["update_id"] + 1
        await asyncio.sleep(1)  # Задержка перед следующим запросом

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(poll_updates())
    asyncio.create_task(check_deadlines(1800, 12))

@app.post("/send_message")
async def get_message(data: SendMessage):
    non_verif = []
    for el in data.ids:
        if check_user_confirmed(str(el)):
            await send_message(el, data.message)
        else:
            non_verif.append(el)
    if non_verif:
        return {
            "message": f"Пользователям с id {non_verif} сообщения отправлены не были, т.к. они не подтвердили telegram аккаунты",
            "status_code": 400
        }
    else:
        return {
            "message": "Сообщения было успешно отправлено",
            "status_code": 200
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
