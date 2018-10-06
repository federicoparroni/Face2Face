import time
import datetime
import socket

import os
from PIL import Image

import telegram


telegram_default_token = '591311395:AAEfSH464BdXSDezWGMZwdiLxLg2_aLlGDE'
telegram_default_chat_id = -1001223624517
telegram_default_timeout = 100


def current_datetime():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def connection_available():
    REMOTE_SERVER = "www.google.com"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


# Send a message through telegram
def telegram_send_msg(message, timeout=telegram_default_timeout, token=telegram_default_token, chat_id=telegram_default_chat_id):
    try:
        bot = telegram.Bot(token=token)
        message = "{} - {}".format(current_datetime(), message)
        bot.send_message(chat_id=chat_id, text=message, timeout=timeout)
    except Exception as err:
        print(err)


#convert an image from png to jpeg
def convert_to_jpg(path):
    extension = path.split('.')[-1]
    extension = extension.lower()
    path_no_extension = path.split('.')[0]
    if extension == 'png' or extension == 'pgm':
        img = Image.open(path)
        img.convert('RGB').save(path_no_extension + '.jpg', 'JPEG')
        os.remove(path)


def convert_to_jpeg_recursive(path):
        entries = os.scandir(path)
        for entry in entries:
            if not entry.is_dir():
                convert_to_jpg(entry.path)
            else:
                convert_to_jpeg_recursive(entry.path)


#convert_to_jpeg_recursive('/home/edoardo/Desktop/Dataset/2_dataset test')