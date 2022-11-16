from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
TOKEN= "5606262089:AAH2n1-azrCJR0dLSKyD4761YhktmJFzRmk"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Salom")
@dp.message_handler(commands=['start', 'help'])
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("salom")


if __name__ == '__main__':
    executor.start_polling(dp)