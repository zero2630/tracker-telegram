import os
import httpx
from fastapi import FastAPI
import asyncio

from conf import TOKEN
import database

app = FastAPI()
BOT_TOKEN = TOKEN
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)