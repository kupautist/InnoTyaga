#!/usr/bin/env python3.12
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)

from botInstance import bot
from commandHandlers import *

def main():
    bot.infinity_polling(logger_level=logging.WARN)

if __name__ == '__main__':
    main()
