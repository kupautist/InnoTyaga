import json
import logging
from kachok import KachokEncoder, kachok_decoder

# list of alias of members who have access to all commands
vip_members = []
try:
    vip_members = [line.strip() for line in open('vip.txt').readlines()]
except Exception as e:
    logging.error(e)
    vip_members = ['kupamonke']  # fallback data

# dictionary that remember information in format user_chat_id:information
# used in functions with register_next_step_handler
user_dict = {}


# dictionary of all members in alias:Kachok format, sorted after any changes
kachki = {}


# done
def do_some_sorting(members):
    """function that sort dictionary by protein points of values, used for sort top"""
    return dict(sorted(members.items(), key=lambda item: item[1].proteinPoints, reverse=True))


def get_sorted(members):
    """function that returns list of Kachok sorted by pp"""
    return sorted(members.values(), key=lambda item: item.proteinPoints, reverse=True)


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
try:
    kachki = {m.alias : m for m in [kachok_decoder(mem) for mem in load_data()]}
except Exception as e:
    logging.error('Unable to load kachki from JSON')
    logging.error(e)
    kachki = {}
    open('kachki.json', 'w').write('[]')
