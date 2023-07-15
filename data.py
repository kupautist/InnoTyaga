import json, logging
from kachok import Kachok, KachokEncoder

# list of alias of members who have access to all commands
vip_members = []
try:
    vip_members = [line.strip() for line in open('vip.txt').readlines()]
except Exception as e:
    logging.error(e)
    vip_members = ['kupamonke'] # fallback data

# dictionary that remember information in format user_chat_id:information
# used in functions with register_next_step_handler
user_dict = {}


# dictionary of all members in alias:Kachok format, sorted after any changes
kachki = {}

def do_some_sorting(members):
    """function that sort dictionary by protein points of values, used for sort top"""
    members = dict(sorted(members.items(), key=lambda item: item[1].proteinPoints, reverse=True))
    return members

def writeData():
    try:
        with open('kachki.json', 'w') as f:
            global kachki
            json.dump(list(kachki.values()), f, cls=KachokEncoder)
            f.flush()
    except Exception as e:
        logging.error(e)

def loadData():
    try:
        with open('kachki.json', 'r') as f:
            global kachki
            # kachki = JSONtoKachki(json.load(f))
    except Exception as e:
        logging.error(e)

# loadData()

def updateRecords():
    """function that updates the records of kachki"""
    global kachki
    kachki = do_some_sorting(kachki)
    writeData()