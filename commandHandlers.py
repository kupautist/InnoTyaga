import logging
import sqlite3

from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telebot.formatting import escape_reserved_markdown

from access import AccessLvl, access_from_str, has_access
from botInstance import bot
from data import Order, get_sorted, kachki, load_kachki, update_records, user_dict
from kachok import Kachok
from Locale import get_locale


def save_some_data():
    connect = sqlite3.connect('kachki.protein')
    cursor = connect.cursor()
    for kachok in kachki.values():
        try:
            cursor.execute('INSERT INTO kachki (id, name, chips, alias) VALUES (?, ?, ?, ?, ?, ?, ?)',
                          (i.chat_id, i.name, i.chips, i.alias))
        except Exception:
            cursor.execute('UPDATE eblans SET name = ?, chips = ?, alias = ? WHERE id = ?',
                          (i.name, i.chips, i.alias, i.chat_id))
    connect.commit()
    return 0


def data_load_decorator(function):
    """decorator that update database after function execution"""
    def wrapper(user):
        function(user)
        save_some_data()
    return wrapper


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """function that greets the user"""
    bot.send_message(message.chat.id, '{}, {} {}{}'.format(
        get_locale(message).greet[0],
        message.from_user.first_name,
        message.from_user.last_name,
        get_locale(message).greet[1]))


@bot.message_handler(commands=['help'])
def commands_list(message: Message) -> None:
    """function that send to user list of possible commands and their description"""
    alias = '@' + message.from_user.username.lower()
    message.from_user.language_code
    if alias not in kachki:
        bot.send_message(message.chat.id, get_locale(message).commands[0])
        bot.send_message(message.chat.id, get_locale(message).reg)
        return
    for i in range(0, kachki[alias].access + 1):
        bot.send_message(message.chat.id,
                         escape_reserved_markdown(get_locale(message).commands[i]),
                         parse_mode='MarkdownV2')


@bot.message_handler(commands=['schedule'])
def schedule(message: Message) -> None:
    """function that send to user schedule of club meetings"""
    bot.send_message(message.chat.id, escape_reserved_markdown(get_locale(message).schedule),
                     parse_mode='MarkdownV2')


@bot.message_handler(commands=['pp'])
def grading(message: Message) -> None:
    """function that send to user grading information"""
    bot.send_message(message.chat.id, get_locale(message).pp)


@bot.message_handler(commands=['top'], chat_types=['private'])
def top(message: Message) -> None:
    """function that display top"""
    global kachki
    counter = 0
    result = ''
    # display all members
    leaderboard = get_sorted(kachki)
    for i in leaderboard:
        result += str(counter + 1) + " " + i.display() + '\n'
        counter += 1
    # in case top empty send message indicating about
    if result == '':
        bot.send_message(message.chat.id, get_locale(message).emptyTop)
    else:
        bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['top'], chat_types=['group', 'supergroup', 'channel'])
def top(message: Message) -> None:
    bot.send_message(message.chat.id, "Пошёл нахуй")


@bot.message_handler(commands=['register'])
def register(message: Message) -> None:
    """function that add to top member who send "/register" message"""
    global kachki
    try:
        # function takes alias and name of user who send this command
        alias = '@' + message.from_user.username.lower()
        name = message.from_user.first_name[:19]
        # add user to top and sort it
        if alias not in kachki:
            kachki[alias] = Kachok(alias, name, message.chat.id)
            bot.send_message(message.chat.id, get_locale(message).newMemberSuccess)
            update_records()
        # if user already in top report about it
        else:
            bot.send_message(message.chat.id, get_locale(message).alreadyRegistred)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).regProblem)


@bot.message_handler(commands=['info'])
def info(message: Message) -> None:
    """function that display personal member profile"""
    global kachki
    try:
        # function takes alias and name of user who send this command
        alias = '@' + message.from_user.username.lower()
        if alias not in kachki:
            bot.send_message(message.chat.id, get_locale(message).reg)
        # if user already in top report about it
        else:
            info = kachki[alias].info(message.from_user.language_code)
            bot.send_message(message.chat.id, info)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).regProblem)


@bot.message_handler(commands=['changename'])
def change_name(message: Message) -> None:
    """function that change member's name"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    # add all aliases of all members to reply keyboard
    rmk = message.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, change_name_answer)


def change_name_answer(message: Message) -> None:
    """next part of change_name"""
    global kachki
    # report if user with such alias not registered
    if message.text not in kachki:
        bot.send_message(message.chat.id, get_locale(message).not_registered)
        return
    # alias saved
    user_dict[message.from_user.id] = message.text
    # clear reply keyboard
    rmk = ReplyKeyboardRemove(selective=False)
    # name requested
    msg = bot.reply_to(message, get_locale(message).enter_name, reply_markup=rmk)
    bot.register_next_step_handler(msg, change_name_answer_2)


def change_name_answer_2(message: Message) -> None:
    """next part of change_name_answer"""
    # check if name too long
    if len(message.text) > 16:
        msg = bot.reply_to(message, get_locale(message).long_name)
        bot.register_next_step_handler(msg, change_name_answer_2)
        return
    global user_dict, kachki
    try:
        # saved information taken
        alias = user_dict[message.from_user.id]
        name = message.text.lower()
        # name changed
        kachki[alias].name = name[0:19]
        update_records()
        bot.send_message(message.chat.id, get_locale(message).success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).exception)
    user_dict[message.from_user.id] = None


@bot.message_handler(commands=['makefemale'])
def make_female(message: Message) -> None:
    """function that can be helpful if * forgotten while adding female member"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    # add all aliases of all members to reply keyboard
    rmk = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, make_female_answer)


def make_female_answer(message: Message) -> None:
    """next part of make_female"""
    # report if user with such alias not registered
    global kachki
    if message.text not in kachki:
        bot.send_message(message.chat.id, get_locale(message).not_registered)
        return
    # alias saved
    user_dict[message.from_user.id] = message.text
    # clear reply keyboard
    rmk = ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, get_locale(message).making_woman, reply_markup=rmk)
    try:
        # alias taken
        alias = user_dict[message.from_user.id]
        # make member female
        kachki[alias].make_female()
        update_records()
        bot.send_message(message.chat.id, get_locale(message).success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).exception)
    user_dict[message.from_user.id] = None


@bot.message_handler(commands=['setweight'])
def set_weight(message: Message) -> None:
    """function that used to change member weight"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    # add all aliases of all members to reply keyboard
    rmk = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer)


def set_weight_answer(message: Message) -> None:
    """next part of set_weight"""
    # report if user with such alias not registered
    global user_dict, kachki
    if message.text not in kachki:
        bot.send_message(message.chat.id, get_locale(message).not_registered)
        return
    # alias saved
    user_dict[message.from_user.id] = message.text
    # clear reply keyboard
    rmk = ReplyKeyboardRemove(selective=False)
    # weight requested
    msg = bot.reply_to(message, get_locale(message).enter_weight, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer_2)


def set_weight_answer_2(message: Message) -> None:
    """next part of set_weight_answer"""
    # check if weight format incorrect
    try:
        float(message.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(message.chat.id, get_locale(message).weight_format)
        bot.register_next_step_handler(msg, set_weight_answer_2)
        return
    global user_dict, kachki
    try:
        # alias taken
        alias = user_dict[message.from_user.id]
        # weight changed
        kachki[alias].set_weight(message.text)
        # update json record
        update_records()
        bot.send_message(message.chat.id, get_locale(message).success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).exception)
    user_dict[message.from_user.id] = None


@bot.message_handler(commands=['setselfweight'])
def set_self_weight(message: Message) -> None:
    """function for changing member self weight"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    # add all aliases of all members to reply keyboard
    rmk = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer)


def setselfweight_answer(message: Message) -> None:
    """next part of set_self_weight"""
    # report if user with such alias not registered
    global user_dict, kachki
    if message.text not in kachki:
        bot.send_message(message.chat.id, get_locale(message).not_registered)
        return
    user_dict[message.from_user.id] = message.text
    # clear reply keyboard
    rmk = ReplyKeyboardRemove(selective=False)
    # self weight requested
    msg = bot.reply_to(message, get_locale(message).enter_self_weight, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer_2)


def setselfweight_answer_2(message: Message) -> None:
    """next part of setselfweight_answer"""
    # check if weight format inncorrect
    try:
        float(message.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(message.chat.id, get_locale(message).weight_format)
        bot.register_next_step_handler(msg, setselfweight_answer_2)
        return
    global user_dict, kachki
    try:
        # alias taken
        alias = user_dict[message.from_user.id]
        # self weight changed
        kachki[alias].set_self_weight(message.text)
        update_records()
        bot.send_message(message.chat.id, get_locale(message).success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).exception)
    user_dict[message.from_user.id] = None


@bot.message_handler(commands=['newuser'])
def new_user(message: Message) -> None:
    """function that add to top new member"""
    # only several users can use this command
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias)
    bot.register_next_step_handler(msg, new_user_answer)


def new_user_answer(message: Message) -> None:
    """next part of new_user"""
    # alias can be written in both ways: with and without @, next if-else handles both ways
    global user_dict
    alias = ('@' + message.text if message.text[0] != '@' else message.text).lower()
    user_dict[message.from_user.id] = alias
    # name requested
    msg = bot.reply_to(message, get_locale(message).enter_name)
    bot.register_next_step_handler(msg, new_user_answer_2)


def new_user_answer_2(message: Message) -> None:
    """next part of new_user_answer"""
    global kachki, user_dict
    try:
        # add to the top new Kachok with received alias and name
        if len(message.text) > 16:
            msg = bot.reply_to(message, get_locale(message).long_name)
            bot.register_next_step_handler(msg, new_user_answer_2)
            return
        name = message.text
        alias = user_dict[message.from_user.id]
        kachki[alias] = Kachok(alias, name)
        update_records()
        bot.send_message(message.chat.id, get_locale(message).success)
        # clear user_dict
        user_dict[message.from_user.id] = None
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).exception)


@bot.message_handler(commands=['danilnikulin', 'DanilNikulin'])
def danil_nikulin(message: Message) -> None:
    """DanilNikulin"""
    for i in range(10):
        bot.send_message(message.chat.id, get_locale(message).nikulin)


@bot.message_handler(commands=['delete'])
def delete_nikulin(message: Message) -> None:
    """function that make able to delete members from top"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    # add all aliases of all members to reply keyboard
    rmk = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, delete_answer)


def delete_answer(message: Message) -> None:
    """next part of delete_nikulin"""
    # clear reply keyboard
    rmk = ReplyKeyboardRemove(selective=False)
    # if member with such alias do not registered, report about it
    global kachki
    if message.text not in kachki:
        bot.reply_to(message, get_locale(message).not_registered, reply_markup=rmk)
        return
    # else delete member with corresponding alias from top
    bot.reply_to(message, get_locale(message).deleting, reply_markup=rmk)
    try:
        alias = message.text
        kachki.pop(alias)
        update_records()
        bot.send_message(message.chat.id, get_locale(message).success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).exception)


@bot.message_handler(commands=['reload'])
def reload(message: Message) -> None:
    """reloads the data from db"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.OWNER):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    load_kachki()
    bot.send_message(message.chat.id, get_locale(message).success)


@bot.message_handler(commands=['stop'])
def stop(message: Message) -> None:
    """reloads the data from db"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.OWNER):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    bot.send_message(message.chat.id, get_locale(message).success)
    bot.stop_polling()


@bot.message_handler(commands=['chaccess'])
def chaccess_nikulin(message: Message) -> None:
    """changes access level of a member"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, message.from_user.username.lower(), AccessLvl.OWNER):
        bot.send_message(message.chat.id, get_locale(message).accessDenied)
        return
    # add all aliases of all members to reply keyboard
    rmk = message.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, chaccess_answer)


def chaccess_answer(message: Message) -> None:
    global user_dict
    alias = '@' + message.text if message.text[0] != '@' else message.text
    user_dict[message.from_user.id] = alias
    # add all access levels to reply keyboard
    levels = [i.name for i in AccessLvl]
    rmk = message.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in levels:
        rmk.add(i)
    # alias requested
    msg = bot.reply_to(message, get_locale(message).enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, chaccess_answer_2)


def chaccess_answer_2(message: Message) -> None:
    global kachki, user_dict
    rmk = ReplyKeyboardRemove(selective=False)
    try:
        alias = user_dict[message.from_user.id]
        kachki[alias].access = access_from_str(message.text)
        user_dict[message.from_user.id] = None
        update_records()
        bot.send_message(message.chat.id, get_locale(message).success, reply_markup=rmk)
    except Exception as e:
        logging.error(e)
        bot.send_message(message.chat.id, get_locale(message).exception, reply_markup=rmk)


@bot.message_handler(content_types=['photo'], chat_types=['private'])
def photo(message: Message) -> None:
    """function that handles photos"""
    bot.reply_to(message, get_locale(message).goodPhoto)


@bot.message_handler(chat_types=['private'])
def wrong_command(message: Message) -> None:
    """function that send to user information that such command did not exist"""
    bot.send_message(message.chat.id, get_locale(message).command_unknown)
