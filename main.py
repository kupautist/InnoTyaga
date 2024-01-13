#!/usr/bin/env python3
import logging

from botInstance import bot
from commandHandlers import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)

def main():
    bot.infinity_polling(logger_level=logging.WARN)

if __name__ == '__main__':
    main()
