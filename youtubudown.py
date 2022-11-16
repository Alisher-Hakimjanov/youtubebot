import logging
import os.path
import random

import pytube
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandHelp, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

TOKEN = "5766883359:AAGpJ2PjYIbW0ElcexKIVDDoaX3ZQpOGlPQ"

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

option_btn  = ReplyKeyboardMarkup(resize_keyboard=True).row((KeyboardButton("📽Video yuklash")),(KeyboardButton("Music yuklash🎵"))).add(KeyboardButton("Info📝")).add(KeyboardButton("Help🔎"))

class DownloadStates(StatesGroup):
    sending_video_url = State()
    sending_music_url  = State()

@dp.message_handler(Text(equals="Info📝",ignore_case=True))
async def get_info(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Salom mening ismim Alisher va bu botni men tayyorladim   @hakimjanov_03')
@dp.message_handler(Text(equals='📽Video yuklash', ignore_case= True))
async  def get_url(msg: types.Message):
    await DownloadStates.sending_video_url.set()
    await bot.send_message(msg.from_user.id,"Please send the url of video to download it from You Tube ")


@dp.message_handler(Text(equals='Music yuklash🎵', ignore_case= True))
async  def get_url(msg: types.Message):
    await DownloadStates.sending_music_url.set()
    await bot.send_message(msg.from_user.id,"Please send the url of video to download it from You Tube ")


@dp.message_handler(state=DownloadStates.sending_video_url)
async def uploadMediaFiles(message: types.Message, state : FSMContext):
    file_name = str(random.randint(0,100000))
    await bot.send_message(message.chat.id, "Yuklanmoqda ...")

    try:
        yt = pytube.YouTube(message.text)
        #yt = yt.streams.filter(only_audio= True, file_extension='mp4').first()
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        path = './videos'
        if not os.path.exists(path):
            os.makedirs(path)
        file_name += '.mp4'
        yt.download(path, filename= file_name)

        logging.info(f'Started processing {file_name}')
        with open(os.path.join(path,file_name),'rb') as file:
            await bot.send_video(message.chat.id, file, disable_notification=True)
            #await bot.send_audio(message.chat.id, file, disable_notification=True)
        await bot.send_message(message.chat.id, "Marhamat !")
    except Exception as ex:
        print(ex)
        await bot.send_message(message.chat.id, "Tarmoqda uzulish kuzatilmaoqda . Qayta urinib koring")

    finally:
        await  state.finish()


@dp.message_handler(state=DownloadStates.sending_music_url)
async def uploadMediaFiles(message: types.Message, state : FSMContext):
    file_name = str(random.randint(0,100000))
    await bot.send_message(message.chat.id, "Downloading ...")

    try:
        yt = pytube.YouTube(message.text)
        yt = yt.streams.filter(only_audio= True, file_extension='mp4').first()
        #yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        path = './videos'
        if not os.path.exists(path):
            os.makedirs(path)
        file_name += '.mp4'
        yt.download(path, filename= file_name)

        logging.info(f'Started processing {file_name}')
        with open(os.path.join(path,file_name),'rb') as file:
            #await bot.send_video(message.chat.id, file, disable_notification=True)
            await bot.send_audio(message.chat.id, file, disable_notification=True)
        await bot.send_message(message.chat.id, "Marhamat !")
    except Exception as ex:
        print(ex)
        await bot.send_message(message.chat.id, "Tarmoqda uzulish kuzatilmaoqda . Qayta urinib koring")

    finally:
        await  state.finish()

@dp.message_handler(Text(equals='Help🔎',ignore_case=True))
async def bot_help(message : types.Message):
    await message.answer('Ushbu bot orqali You Tubedagi istalgan audio va videolarni  yuklashingiz mumkin /download_youtube_video')


@dp.message_handler(commands=['start'])
async def on_start(msg:types.Message):
    await bot.send_message(msg.from_user.id, "Salom siz bu bot orqali You Tube dagi ustagan videolarni yuklashingiz mumkin  ! \n/help", reply_markup=option_btn)


if __name__ == '__main__':
    executor.start_polling(dp)

