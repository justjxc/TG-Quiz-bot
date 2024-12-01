import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
load_dotenv()

from handlers import router

API_TOKEN = os.environ["API_TOKEN"]

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

dp.include_router(router)