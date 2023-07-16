import os
from dotenv import load_dotenv
import telebot

load_dotenv('.env')
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
