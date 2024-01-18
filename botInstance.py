import os
from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv('.env')
bot = TeleBot(os.environ.get('BOT_TOKEN'))
