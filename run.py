#!/usr/bin/env python3.12
import logging
import sqlite3
from data import kachki
from botInstance import bot
from commandHandlers import *
from kachok import Kachok
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)


def main():
    bot.infinity_polling(logger_level=logging.WARN)
    connect = sqlite3.connect('kachki.protein')
    cur = connect.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS kachki (name varchar(20), alias varchar(32), chat_id int primary key, access int'
        ', selfWeight float, weights varchar(15), mark varchar(1))'
    )
    # load_some_data
    cur.execute('SELECT * FROM kachki')
    users = cur.fetchall()
    for user in users:
        kachok = Kachok(user[1], user[0], user[2])
        if user[3] == 0:
            kachok.access = AccessLvl.MEMBER
        elif user[3] == 1:
            AccessLvl.VIP
        else:
            kachok.access = AccessLvl.OWNER
        kachok.selfWeight = user[4]
        kachok.weights['bench press'], kachok.weights['squat'], kachok.weights['biceps curl'] = user[5].split()
        kachok.mark = user[6]
        kachki[user[1]] = kachok
    connect.commit()


if __name__ == '__main__':
    main()
