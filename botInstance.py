import os
from dotenv import load_dotenv
import telebot

load_dotenv('.env')
token = os.environ.get('BOT_TOKEN')
assert token is not None, "Token is not defined"
bot = telebot.TeleBot(token)
