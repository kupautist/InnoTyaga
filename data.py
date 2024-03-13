import json
import logging
import os
from enum import IntEnum, auto
from typing import Any
from telebot.types import Message

from kachok import Kachok, KachokEncoder, kachok_decoder

# dictionary that remember information in format user_chat_id:information
# used in functions with register_next_step_handler
user_dict: dict[str, Message] = {}

# dictionary of all members in alias:Kachok format, sorted after any changes
kachki: dict[str, Kachok] = {}

class Order(IntEnum):
    PP = auto()
    ALPHABETICAL = auto()
    SELF_WEIGHT = auto()


def get_sorted(members: dict[str, Kachok], order = Order.PP) -> list[Kachok]:
    """function that returns list of Kachok sorted by parameter order (by defult PP)"""
    match order:
        case Order.PP:
            return sorted(members.values(), key=lambda item: item.proteinPoints, reverse=True)
        case Order.ALPHABETICAL:
            return sorted(members.values(), key=lambda item: item.alias)
        case Order.SELF_WEIGHT:
            return sorted(members.values(), key=lambda item: item.selfWeight, reverse=True)
        case _:
            raise ValueError("Wrong order argument in get_sorted()")


def write_data() -> None:
    """function that dumps kachki dictionary into a kachki.json"""
    try:
        with open('kachki.json', 'w') as f:
            global kachki
            json.dump(list(kachki.values()), f, cls=KachokEncoder)
            f.flush()
    except Exception as e:
        logging.error(e)


def load_data(filename: str = 'kachki.json') -> list[dict[str, Any]]:
    if not os.path.isfile(filename):
        raise FileNotFoundError(f'The {filename} does not exist')
    return json.load(open(filename, 'r'))


def update_records() -> None:
    """function that updates the records of kachki"""
    write_data()


# Load Kachki
def load_kachki() -> None:
    global kachki
    try:
        kachki = {m.alias : m for m in [kachok_decoder(mem) for mem in load_data()]}
    except IOError as e:
        logging.error('Unable to read JSON')
        logging.error(e)
        kachki = {}
        open('kachki.json', 'w').write('[]')
    except Exception as e:
        logging.error('Unable to load kachki from JSON')
        logging.error(e)
        kachki = {}


def merge_kachki(filename: str = 'kachki_new.json') -> None:
    global kachki
    kachki_new: dict[str, Kachok] = {}
    try:
        kachki_new = {m.alias : m for m in [kachok_decoder(mem) for mem in load_data(filename)]}
    except IOError as e:
        logging.error('Unable to read JSON while merging db')
        logging.error(e)
    except Exception as e:
        logging.error('Unable to load kachki_new from JSON while merging db')
        logging.error(e)
    try:
        for k in kachki_new.values():
            if k.alias not in kachki:
                kachki[k.alias] = k
            elif (k != kachki[k.alias]):
                kachki[k.alias].alias = k.alias
                kachki[k.alias].name = k.name
                kachki[k.alias].female = k.female
                kachki[k.alias].access = k.access
                kachki[k.alias].selfWeight = k.selfWeight
                kachki[k.alias].weight = max(k.weight, kachki[k.alias].weight)
                kachki[k.alias].proteinPoints = max(k.proteinPoints, kachki[k.alias].proteinPoints)
                kachki[k.alias].mark = max(k.mark, kachki[k.alias].mark)
                kachki[k.alias].proteinPointsByDate = kachki[k.alias].proteinPointsByDate | k.proteinPointsByDate
                kachki[k.alias].weightByDate = kachki[k.alias].weightByDate | k.weightByDate
                kachki[k.alias].selfWeightByDate = kachki[k.alias].selfWeightByDate | k.selfWeightByDate
    except Exception as e:
        logging.error('Exception caught while merging db')
        logging.error(e)

load_kachki()
if (os.path.isfile('kachki_new.json')):
    merge_kachki()
    update_records()
    os.remove('kachki_new.json')
