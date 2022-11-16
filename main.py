import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "5606262089:AAH2n1-azrCJR0dLSKyD4761YhktmJFzRmk"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
API_KEY = "ec6b8d18f766e01fdec86a74bd046289"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

#viloyatlar = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("tashkent",request_location=True)).add(KeyboardButton("Samarqand", request_location=True))
#tugma = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🌎 Share Location", request_location=True)).add(KeyboardButton("Telefon raqam yuboring", request_contact=True))
tillar = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("English", request_language=True)).add(KeyboardButton("Rus tili",request_language= True)).add(KeyboardButton("Uzbek",request_language=True))

@dp.message_handler()
async def process_message(msg: types.Message):
    city = msg.text
    requests_url = f'{BASE_URL}?appid={API_KEY}&q={city}'
    response = requests.get(requests_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = round(data['main']['temp'] - 273.15, 2)
        result = "Weather: " + weather + "\nTemperature: " + str(temperature)
        await bot.send_message(msg.from_user.id, result, reply_markup=tillar)
    else:
        print("Error.")

if __name__ == '__main__':
    executor.start_polling(dp)