import json
import logging
from enum import IntEnum, auto
from kachok import KachokEncoder, kachok_decoder

# dictionary that remember information in format user_chat_id:information
# used in functions with register_next_step_handler
user_dict = {}

# dictionary of all members in alias:Kachok format, sorted after any changes
kachki = {}

class Order(IntEnum):
    PP = auto()
    ALPHABETICAL = auto()
    SELF_WEIGHT = auto()


def get_sorted(members, order = Order.PP) -> list:
    """function that returns list of Kachok sorted by parameter order (by defult PP)"""
    match order:
        case Order.PP:
            return sorted(members.values(), key=lambda item: item.proteinPoints, reverse=True)
        case Order.ALPHABETICAL:
            return sorted(members.values(), key=lambda item: item.alias)
        case Order.SELF_WEIGHT:
            return sorted(members.value(), key=lambda item: item.selfWeight, reverse=True)
        case _:
            return None


def write_data():
    """function that dumps kachki dictionary into a kachki.json"""
    try:
        with open('kachki.json', 'w') as f:
            global kachki
            json.dump(list(kachki.values()), f, cls=KachokEncoder)
            f.flush()
    except Exception as e:
        logging.error(e)


def load_data():
    try:
        with open('kachki.json', 'r') as f:
            global kachki
            return json.load(f)
    except Exception as e:
        logging.error(e)
        return None


def update_records():
    """function that updates the records of kachki"""
    global kachki
    write_data()


# Load Kachki
def load_kachki():
    global kachki
    try:
        kachki = {m.alias : m for m in [kachok_decoder(mem) for mem in load_data()]}
    except Exception as e:
        logging.error('Unable to load kachki from JSON')
        logging.error(e)
        kachki = {}
        open('kachki.json', 'w').write('[]')


load_kachki()
