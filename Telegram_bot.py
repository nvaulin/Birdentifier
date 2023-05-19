import os
import sys
import time
import datetime
import io
import requests
import random
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from model import identify_class

load_dotenv()
bot_token = os.environ.get('TG_API_TOKEN')
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# 🐤🐤🐧🐧🐦🐔🐦🐣🐥🐣🐤🦆🦅🦉
with open(os.path.join('messages', 'start_help_messages.txt'), 'r') as file:
    messages = file.read().splitlines()
     
with open(os.path.join('messages', 'text_messages.txt'), 'r') as file:
    texts_replies = file.read().splitlines()

@dp.message_handler(commands=["start"]) 
async def command_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/help", "/start"]
    keyboard.add(*buttons)
    await message.answer(random.choice(messages), reply_markup=keyboard)

@dp.message_handler(commands=["help"])
async def command_help(message: types.Message):
        await message.answer(random.choice(messages))

@dp.message_handler()
async def reply_on_text(message: types.Message):
        await message.answer(random.choice(texts_replies))

@dp.message_handler(content_types=['photo'])
async def process_photo(messsage: types.Message):
        await messsage.photo[-1].download(f"{messsage.message_id}.jpg")
        name = identify_class(f"{messsage.message_id}.jpg")
        await dp.bot.send_message(chat_id=messsage.from_user.id, text=name)


executor.start_polling(dp, skip_updates=True)