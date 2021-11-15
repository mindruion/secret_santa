from fastapi import FastAPI, Request
from telegram.ext import Updater

app = FastAPI()


@app.post("/")
async def root(request: Request):
    data = await request.json()
    updater = Updater("2142480007:AAG_VYXS4P8f-0IWJwhJWXCFCO5NyWBV0Xw")
    updater.bot.send_message(data['message']['chat']['id'], data)
    return {"message": "Hello World"}