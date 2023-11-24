import logging
from telebot import types
from kachok import Kachok
from access import *
from staticText import *
from botInstance import bot
from data import kachki, user_dict, update_records, get_sorted, Order, load_kachki


@bot.message_handler(commands=['start', 'начать'])
def start(user):
    """function that greets the user"""
    bot.send_message(user.chat.id, f'Здарова, {user.from_user.first_name} {user.from_user.last_name}' + RU.greet)


@bot.message_handler(commands=['gradeall'])
def grade_all(user):
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.OWNER):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    for i in kachki:
        kachki.get(i).grade()
    bot.send_message(user.chat.id, "Все, я всех загредил")


@bot.message_handler(commands=['scalepoints'])
def scale_points(user):
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.OWNER):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    for i in kachki:
        kachki.get(i).proteinPoints *= 0.5
        kachki.get(i).grade()
    bot.send_message(user.chat.id, "Все, я всех загредил")


@bot.message_handler(commands=['help', 'помощь'])
def commands_list(user):
    """function that send to user list of possible commands and their description"""
    alias = '@' + user.from_user.username.lower()
    if alias not in kachki:
        bot.send_message(user.chat.id, RU.commands[0])
        bot.send_message(user.chat.id, RU.reg)
        return
    for i in range(0, kachki[alias].access + 1):
        bot.send_message(user.chat.id, RU.commands[i])


@bot.message_handler(commands=['schedule'])
def schedule(user):
    """function that send to user schedule of club meetings"""
    bot.send_message(user.chat.id, RU.schedule_)


@bot.message_handler(commands=['pp'])
def grading(user):
    """function that send to user grading information"""
    bot.send_message(user.chat.id, RU.pp)


@bot.message_handler(commands=['top'])
def top(user):
    """function that display top"""
    global kachki
    counter = 0
    result = ''
    # display all members
    leaderboard = get_sorted(kachki)
    for i in leaderboard:
        if i.proteinPoints != 0:
            result += str(counter + 1) + " " + i.display() + '\n'
            counter += 1
    # in case top empty send message indicating about
    if result == '':
        bot.send_message(user.chat.id, RU.emptyTop)
    else:
        bot.send_message(user.chat.id, result)


@bot.message_handler(commands=['register'])
def register(user):
    """function that add to top member who send "/register" message"""
    global kachki
    try:
        # function takes alias and name of user who send this command
        alias = '@' + user.from_user.username.lower()
        name = user.from_user.first_name
        # add user to top and sort it
        if alias not in kachki:
            kachki[alias] = Kachok(alias, name)
            bot.send_message(user.chat.id, RU.newMemberSuccess)
            update_records()
        # if user already in top report about it
        else:
            bot.send_message(user.chat.id, RU.newMemberFail)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.regProblem)


@bot.message_handler(commands=['info'])
def info(user):
    """function that display personal member profile"""
    global kachki
    try:
        # function takes alias and name of user who send this command
        alias = '@' + user.from_user.username.lower()
        if alias not in kachki:
            bot.send_message(user.chat.id, RU.reg)
        # if user already in top report about it
        else:
            info = kachki[alias].info()
            bot.send_message(user.chat.id, info)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.regProblem)


@bot.message_handler(commands=['olduser'])
def old_user(user):
    """part 1 of function that add to top old member"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # member's alias requested
    msg = bot.reply_to(user, RU.enter_alias)
    bot.register_next_step_handler(msg, olduser_answer)


def olduser_answer(user):
    """part 2 of function that add to top old member"""
    # alias can be written in both ways: with and without @, next if-else handles both
    # member's alias saved
    global user_dict, kachki
    alias = '@' + user.text if user.text[0] != '@' else user.text
    user_dict[user.chat.id] = alias.lower()
    print(user_dict[user.chat.id])
    if user_dict[user.chat.id][0] in kachki:
        msg = bot.reply_to(user, RU.newMemberFail)
        bot.register_next_step_handler(msg, olduser_answer)
    # member's name requested
    msg = bot.reply_to(user, RU.enter_name)
    bot.register_next_step_handler(msg, olduser_answer_2)


def olduser_answer_2(user):
    """part 3 of function that add to top old member"""
    # check if name too long
    global user_dict
    if len(user.text) > 16:
        msg = bot.reply_to(user, RU.long_name)
        bot.register_next_step_handler(msg, olduser_answer_2)
        return 0
    # member's name saved
    user_dict[user.chat.id].append(user.text)
    # member's self weight requested
    msg = bot.reply_to(user, RU.enter_self_weight)
    bot.register_next_step_handler(msg, olduser_answer_3)


def olduser_answer_3(user):
    """part 4 of function that add to top old member"""
    # check if self weight format incorrect
    global user_dict
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, RU.weight_format)
        bot.register_next_step_handler(msg, olduser_answer_3)
        return 0
    # member's self weight saved
    user_dict[user.chat.id].append(user.text)
    # member's weight requested
    msg = bot.reply_to(user, RU.enter_weight)
    bot.register_next_step_handler(msg, olduser_answer_4)


def olduser_answer_4(user):
    """part 5 of function that add to top old member"""
    global user_dict, kachki
    # check if weight format incorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, RU.weight_format)
        bot.register_next_step_handler(msg, olduser_answer_4)
        return 0
    # member's weight saved
    user_dict[user.chat.id].append(user.text)
    try:
        # saved information taken
        alias, name, self_weight, weight = user_dict[user.chat.id]
        alias = alias.lower()
        # information about new member added to top
        member = Kachok(alias, name)
        member.set_self_weight(self_weight)
        member.set_weight(weight)
        kachki[alias] = member
        bot.send_message(user.chat.id, RU.newMemberSuccess)
        update_records()
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)
    user_dict[user.chat.id] = None


@bot.message_handler(commands=['changealias'])
def change_alias(user):
    """function that make member's alias lowercase, was created due to error """
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, change_alias_answer)


def change_alias_answer(user):
    """next part of change_name"""
    global kachki
    # report if user with such alias not registered
    if user.text not in kachki:
        bot.send_message(user.chat.id, RU.not_registered)
        return 0
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    if user.text.lower() not in kachki:
        kachki[user.text].alias = user.text.lower()
        msg = bot.reply_to(user, RU.enter_new_alias, reply_markup=rmk)
    else:
        msg = bot.reply_to(user, 'Сначала удали дубликат', reply_markup=rmk)


@bot.message_handler(commands=['changename'])
def change_name(user):
    """function that change member's name"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, change_name_answer)


def change_name_answer(user):
    """next part of change_name"""
    global kachki
    # report if user with such alias not registered
    if user.text not in kachki:
        bot.send_message(user.chat.id, RU.not_registered)
        return 0
    # alias saved
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # name requested
    msg = bot.reply_to(user, RU.enter_name, reply_markup=rmk)
    bot.register_next_step_handler(msg, change_name_answer_2)


def change_name_answer_2(user):
    """next part of change_name_answer"""
    # check if name too long
    if len(user.text) > 16:
        msg = bot.reply_to(user, RU.long_name)
        bot.register_next_step_handler(msg, change_name_answer_2)
        return 0
    global user_dict, kachki
    try:
        # saved information taken
        alias, name = user_dict[user.chat.id], user.text.lower()
        # name changed
        kachki.get(alias).set_name(name)
        update_records()
        bot.send_message(user.chat.id, RU.success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)
    user_dict[user.chat.id] = None


@bot.message_handler(commands=['makefemale'])
def make_female(user):
    """function that can be helpful if * forgotten while adding female member"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, make_female_answer)


def make_female_answer(user):
    """next part of make_female"""
    # report if user with such alias not registered
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, RU.not_registered)
        return 0
    # alias saved
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(user, RU.making_woman, reply_markup=rmk)
    try:
        # alias taken
        alias = user_dict[user.chat.id]
        # make member female
        kachki.get(alias).make_female()
        update_records()
        bot.send_message(user.chat.id, RU.success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)
    user_dict[user.chat.id] = None


@bot.message_handler(commands=['changeweight'])
def change_weight(user):
    """function that used to change member weight"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer)


def change_weight_answer(user):
    """next part of set_weight"""
    # report if user with such alias not registered
    global user_dict, kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, RU.not_registered)
        return 0
    # alias saved
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # weight requested
    msg = bot.reply_to(user, RU.enter_weight, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer_2)


def change_weight_answer_2(user):
    """next part of set_weight_answer"""
    # check if weight format incorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, RU.weight_format)
        bot.register_next_step_handler(msg, set_weight_answer_2)
        return 0
    global user_dict, kachki
    try:
        # alias taken
        alias = user_dict[user.chat.id]
        # weight changed
        kachki.get(alias).change_weight(user.text)
        # update json record
        update_records()
        bot.send_message(user.chat.id, RU.success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)
    user_dict[user.chat.id] = None

@bot.message_handler(commands=['setweight'])
def set_weight(user):
    """function that used to change member weight"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer)


def set_weight_answer(user):
    """next part of set_weight"""
    # report if user with such alias not registered
    global user_dict, kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, RU.not_registered)
        return 0
    # alias saved
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # weight requested
    msg = bot.reply_to(user, RU.enter_weight, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer_2)


def set_weight_answer_2(user):
    """next part of set_weight_answer"""
    # check if weight format incorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, RU.weight_format)
        bot.register_next_step_handler(msg, set_weight_answer_2)
        return 0
    global user_dict, kachki
    try:
        # alias taken
        alias = user_dict[user.chat.id]
        # weight changed
        kachki.get(alias).set_weight(user.text)
        # update json record
        update_records()
        bot.send_message(user.chat.id, RU.success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)
    user_dict[user.chat.id] = None


@bot.message_handler(commands=['setselfweight'])
def set_self_weight(user):
    """function for changing member self weight"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer)


def setselfweight_answer(user):
    """next part of set_self_weight"""
    # report if user with such alias not registered
    global user_dict, kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, RU.not_registered)
        return 0
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # self weight requested
    msg = bot.reply_to(user, RU.enter_self_weight, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer_2)


def setselfweight_answer_2(user):
    """next part of setselfweight_answer"""
    # check if weight format inncorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, RU.weight_format)
        bot.register_next_step_handler(msg, setselfweight_answer_2)
        return 0
    global user_dict, kachki
    try:
        # alias taken
        alias = user_dict[user.chat.id]
        # self weight changed
        kachki.get(alias).set_self_weight(user.text)
        update_records()
        bot.send_message(user.chat.id, RU.success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)
    user_dict[user.chat.id] = None


@bot.message_handler(commands=['newuser'])
def new_user(user):
    """function that add to top new member"""
    # only several users can use this command
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias)
    bot.register_next_step_handler(msg, new_user_answer)


def new_user_answer(user):
    """next part of new_user"""
    # alias can be written in both ways: with and without @, next if-else handles both ways
    global user_dict
    alias = '@' + user.text if user.text[0] != '@' else user.text
    user_dict[user.chat.id] = alias.lower()
    # name requested
    msg = bot.reply_to(user, RU.enter_name)
    bot.register_next_step_handler(msg, new_user_answer_2)


def new_user_answer_2(user):
    """next part of new_user_answer"""
    global kachki, user_dict
    try:
        # add to the top new Kachok with received alias and name
        name = user.text
        alias = user_dict[user.chat.id]
        kachki[alias] = Kachok(alias, name)
        update_records()
        bot.send_message(user.chat.id, RU.success)
        # clear user_dict
        user_dict[user.chat.id] = None
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)


@bot.message_handler(commands=['danilnikulin', 'DanilNikulin'])
def danil_nikulin(user):
    """DanilNikulin"""
    for i in range(10):
        bot.send_message(user.chat.id, RU.nikulin)


@bot.message_handler(commands=['delete'])
def delete_nikulin(user):
    """function that make able to delete members from top"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.VIP):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, delete_answer)


def delete_answer(user):
    """next part of delete_nikulin"""
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # if member with such alias do not registered, report about it
    global kachki
    if user.text not in kachki:
        bot.reply_to(user, RU.not_registered, reply_markup=rmk)
        return 0
    # else delete member with corresponding alias from top
    bot.reply_to(user, RU.deleting, reply_markup=rmk)
    try:
        alias = user.text
        kachki.pop(alias)
        update_records()
        bot.send_message(user.chat.id, RU.success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception)


@bot.message_handler(commands=['reload'])
def reload(user):
    """reloads the data from db"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.OWNER):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    kachki = None
    load_kachki()
    bot.send_message(user.chat.id, RU.success)


@bot.message_handler(commands=['chaccess'])
def chaccess_nikulin(user):
    """changes access level of a member"""
    # only several users can use this command
    global kachki
    if not has_access(kachki, user.from_user.username.lower(), AccessLvl.OWNER):
        bot.send_message(user.chat.id, RU.accessDenied)
        return 0
    # add all aliases of all members to reply keyboard
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in get_sorted(kachki, Order.ALPHABETICAL):
        rmk.add(i.alias)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, chaccess_answer)


def chaccess_answer(user):
    global user_dict
    alias = '@' + user.text if user.text[0] != '@' else user.text
    user_dict[user.chat.id] = alias
    # add all access levels to reply keyboard
    levels = [i.name for i in AccessLvl]
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in levels:
        rmk.add(i)
    # alias requested
    msg = bot.reply_to(user, RU.enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, chaccess_answer_2)
   

def chaccess_answer_2(user):
    global kachki, user_dict
    rmk = types.ReplyKeyboardRemove(selective=False)
    try:
        alias = user_dict[user.chat.id]
        kachki[alias].access = access_from_str(user.text)
        user_dict[user.chat.id] = None
        update_records()
        bot.send_message(user.chat.id, RU.success, reply_markup=rmk)
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, RU.exception, reply_markup=rmk)


@bot.message_handler()
def wrong_command(user):
    """function that send to user information that such command did not exist"""
    bot.send_message(user.chat.id, RU.empty)


@bot.message_handler(content_types=['photo'])
def photo(user):
    """function that handles photos"""
    bot.reply_to(user, RU.goodPhoto)
