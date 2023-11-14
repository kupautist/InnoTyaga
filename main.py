import logging
from botInstance import bot
from commandHandlers import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)



bot.infinity_polling(logger_level=logging.WARN)
