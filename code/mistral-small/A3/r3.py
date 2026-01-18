import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
ADMINS = ['ADMIN_USERNAME']

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.middleware_stack.insert(0, LoggingMiddleware())
scheduler = AsyncIOScheduler()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Hello! How can I help you today?')

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.lower() == 'exit':
        await message.reply('Goodbye!')
    else:
        await message.reply(message.text)

if __name__ == '__main__':
    scheduler.add_job(echo, trigger='interval', seconds=10)
    executor.start_polling(dp, skip_updates=True)