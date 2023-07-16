import logging
from telebot import types
from kachok import Kachok
from staticText import *
from botInstance import bot
from data import kachki, user_dict, vip_members, updateRecords, get_sorted


# done
@bot.message_handler(commands=['start', 'начать'])
def start(user):
    """function that greets the user"""
    bot.send_message(user.chat.id, f'Здарова, {user.from_user.first_name} {user.from_user.last_name}' + greet)


# done
@bot.message_handler(commands=['help', 'помощь'])
def commands_list(user):
    """function that send to user list of possible commands and their description"""
    bot.send_message(user.chat.id, commands)


# done
@bot.message_handler(commands=['schedule'])
def schedule(user):
    """function that send to user schedule of club meetings"""
    bot.send_message(user.chat.id, schedule_)


# done
@bot.message_handler(commands=['pp'])
def grading(user):
    """function that send to user grading information"""
    bot.send_message(user.chat.id, pp)


# done
@bot.message_handler(commands=['top'])
def top(user):
    """function that display top"""
    global kachki
    counter = 0
    result = ''
    # display all members
    for i in get_sorted(kachki):
        result += str(counter + 1) + " " + i.display() + '\n'
        counter += 1
    # in case top empty send message indicating about
    if result == '':
        bot.send_message(user.chat.id, emptyTop)
    else:
        bot.send_message(user.chat.id, result)


# done
@bot.message_handler(commands=['register'])
def register(user):
    """function that add to top member who send "/register" message"""
    global kachki
    try:
        # function takes alias and name of user who send this command
        alias = user.from_user.username
        alias = '@' + alias
        alias = alias.lower()
        name = user.from_user.first_name
        # add user to top and sort it
        if alias not in kachki:
            member = Kachok(alias, name)
            kachki[alias] = member
            bot.send_message(user.chat.id, newMemberSuccess)
            updateRecords()
        # if user already in top report about it
        else:
            bot.send_message(user.chat.id, newMemberFail)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, regProblem)


# done
@bot.message_handler(commands=['olduser'])
def old_user(user):
    """part 1 of function that add to top old member"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    # member's alias requested
    global kachki
    msg = bot.reply_to(user, enter_alias)
    bot.register_next_step_handler(msg, olduser_answer)


def olduser_answer(user):
    """part 2 of function that add to top old member"""
    # alias can be written in both ways: with and without @, next if-else handles both
    # member's alias saved
    if user.text[0] != '@':
        user_dict[user.chat.id] = '@' + user.text
    else:
        user_dict[user.chat.id] = user.text
    if user_dict[user.chat.id] in kachki:
        msg = bot.reply_to(user, newMemberFail)
        bot.register_next_step_handler(msg, olduser_answer)
    # member's name requested
    msg = bot.reply_to(user, enter_name)
    bot.register_next_step_handler(msg, olduser_answer_2)


def olduser_answer_2(user):
    """part 3 of function that add to top old member"""
    # check if name include space
    for i in user.text:
        if ord(i) == 32:
            msg = bot.reply_to(user, no_spaces)
            bot.register_next_step_handler(msg, olduser_answer_2)
            return 0
    # check if name too long
    if len(user.text) > 16:
        msg = bot.reply_to(user, long_name)
        bot.register_next_step_handler(msg, olduser_answer_2)
        return 0
    # member's name saved
    user_dict[user.chat.id] += ' ' + user.text
    # member's self weight requested
    msg = bot.reply_to(user, enter_self_weight)
    bot.register_next_step_handler(msg, olduser_answer_3)


def olduser_answer_3(user):
    """part 4 of function that add to top old member"""
    # check if self weight format incorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, weight_format)
        bot.register_next_step_handler(msg, olduser_answer_3)
        return 0
    # member's self weight saved
    user_dict[user.chat.id] += ' ' + user.text
    # member's weight requested
    msg = bot.reply_to(user, enter_weight)
    bot.register_next_step_handler(msg, olduser_answer_4)


def olduser_answer_4(user):
    """part 5 of function that add to top old member"""
    global kachki
    # check if weight format incorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, weight_format)
        bot.register_next_step_handler(msg, olduser_answer_4)
        return 0
    # member's weight saved
    user_dict[user.chat.id] += ' ' + user.text
    try:
        # saved information taken
        alias, name, self_weight, weight = user_dict[user.chat.id].split()
        alias = alias.lower()
        # information about new member added to top
        member = Kachok(alias, name)
        member.set_self_weight(self_weight)
        member.set_weight(weight)
        kachki[alias] = member
        bot.send_message(user.chat.id, newMemberSuccess)
        # sort top
        updateRecords()
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, exception)
    user_dict[user.chat.id] = ''


# done
@bot.message_handler(commands=['changename'])
def change_name(user):
    """function that change member's name"""
    # only several users can use this command
    global kachki
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    # add all aliases of all members to reply keyboard
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    # alias requested
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, change_name_answer)


def change_name_answer(user):
    """next part of change_name"""
    global kachki
    # report if user with such alias not registered
    if user.text not in kachki:
        bot.send_message(user.chat.id, not_registered)
        return 0
    # alias saved
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # name requested
    msg = bot.reply_to(user, enter_name, reply_markup=rmk)
    bot.register_next_step_handler(msg, change_name_answer_2)


def change_name_answer_2(user):
    """next part of change_name_answer"""
    # check if name include space
    for i in user.text:
        if ord(i) == 32:
            msg = bot.reply_to(user, no_spaces)
            bot.register_next_step_handler(msg, change_name_answer_2)
            return 0
    # check if name too long
    if len(user.text) > 16:
        msg = bot.reply_to(user, long_name)
        bot.register_next_step_handler(msg, change_name_answer_2)
        return 0
    # name saved
    user_dict[user.chat.id] += ' ' + user.text
    global kachki
    try:
        # saved information taken
        alias, name = user_dict[user.chat.id].split()
        alias = alias.lower()
        # name changed
        kachki.get(alias).set_name(name)
        bot.send_message(user.chat.id, success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, exception)
    user_dict[user.chat.id] = ''


# done
@bot.message_handler(commands=['makefemale'])
def make_female(user):
    """function that can be helpful if * forgotten while adding female member"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    # add all aliases of all members to reply keyboard
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    # alias requested
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, make_female_answer)


def make_female_answer(user):
    """next part of make_female"""
    # report if user with such alias not registered
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, not_registered)
        return 0
    # alias saved
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(user, making_woman, reply_markup=rmk)
    try:
        # alias taken
        alias = user_dict[user.chat.id]
        # make member female
        kachki.get(alias).make_female()
        bot.send_message(user.chat.id, success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, exception)
    user_dict[user.chat.id] = ''


# done
@bot.message_handler(commands=['setweight'])
def set_weight(user):
    """function that used to change member weight"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    # add all aliases of all members to reply keyboard
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    # alias requested
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer)


def set_weight_answer(user):
    """next part of set_weight"""
    # report if user with such alias not registered
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, not_registered)
        return 0
    # alias saved
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # weight requested
    msg = bot.reply_to(user, enter_weight, reply_markup=rmk)
    bot.register_next_step_handler(msg, set_weight_answer_2)


def set_weight_answer_2(user):
    """next part of set_weight_answer"""
    # check if weight format incorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, weight_format)
        bot.register_next_step_handler(msg, set_weight_answer_2)
        return 0
    global kachki
    try:
        # alias taken
        alias = user_dict[user.chat.id]
        # weight changed
        kachki.get(alias).set_weight(user.text)
        # sort top
        updateRecords()
        bot.send_message(user.chat.id, success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, exception)
    user_dict[user.chat.id] = ''


# done
@bot.message_handler(commands=['setselfweight'])
def set_self_weight(user):
    """function for changing member self weight"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    # add all aliases of all members to reply keyboard
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    # alias requested
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer)


def setselfweight_answer(user):
    """next part of set_self_weight"""
    # report if user with such alias not registered
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, not_registered)
        return 0
    user_dict[user.chat.id] = user.text
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # self weight requested
    msg = bot.reply_to(user, enter_self_weight, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer_2)


def setselfweight_answer_2(user):
    """next part of setselfweight_answer"""
    # check if weight format inncorrect
    try:
        float(user.text)
    except ValueError as e:
        logging.info(e)
        msg = bot.send_message(user.chat.id, weight_format)
        bot.register_next_step_handler(msg, setselfweight_answer_2)
        return 0
    global kachki
    try:
        # alias taken
        alias = user_dict[user.chat.id]
        # self weight changed
        kachki.get(alias).set_self_weight(user.text)
        bot.send_message(user.chat.id, success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, exception)
    user_dict[user.chat.id] = ''


# done
@bot.message_handler(commands=['newuser'])
def new_user(user):
    """function that add to top new member"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    # alias requested
    msg = bot.reply_to(user, enter_alias)
    bot.register_next_step_handler(msg, new_user_answer)


def new_user_answer(user):
    """next part of new_user"""
    # alias can be written in both ways: with and without @, next if-else handles both ways
    if user.text[0] != '@':
        user_dict[user.chat.id] = '@' + user.text
    else:
        user_dict[user.chat.id] = user.text
    # name requested
    msg = bot.reply_to(user, enter_name)
    bot.register_next_step_handler(msg, new_user_answer_2)


def new_user_answer_2(user):
    """next part of new_user_answer"""
    global kachki
    try:
        # add to the top new Kachok with received alias and name
        name = user.text
        alias = user_dict[user.chat.id]
        member = Kachok(alias, name)
        kachki[alias] = member
        bot.send_message(user.chat.id, success)
        # clear user_dict
        user_dict[user.chat.id] = ''
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, exception)


# done
@bot.message_handler(commands=['danilnikulin', 'DanilNikulin'])
def danil_nikulin(user):
    """DanilNikulin"""
    for i in range(10):
        bot.send_message(user.chat.id, nikulin)


# done
@bot.message_handler(commands=['sort'])
def sort_nikulin(user):
    """function that able to call do_some_sorting from telegram"""
    global kachki
    updateRecords()
    bot.send_message(user.chat.id, sorted_end)


# done
@bot.message_handler(commands=['delete'])
def delete_nikulin(user):
    """function that make able to delete members from top"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    # add all aliases of all members to reply keyboard
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    # alias requested
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, delete_answer)


def delete_answer(user):
    """next part of delete_nikulin"""
    # clear reply keyboard
    rmk = types.ReplyKeyboardRemove(selective=False)
    # if member with such alias do not registered, report about it
    global kachki
    if user.text not in kachki:
        bot.reply_to(user, not_registered, reply_markup=rmk)
        return 0
    # else delete member with corresponding alias from top
    bot.reply_to(user, deleting, reply_markup=rmk)
    try:
        alias = user.text
        kachki.pop(alias)
        bot.send_message(user.chat.id, success)
    # report about if happen something unexpected
    except Exception as e:
        logging.error(e)
        bot.send_message(user.chat.id, exception)


# done
@bot.message_handler()
def wrong_command(user):
    """function that send to user information that such command did not exist"""
    bot.send_message(user.chat.id, empty)


# done
@bot.message_handler(content_types=['photo'])
def photo(user):
    """function that handles photos"""
    bot.reply_to(user, goodPhoto)
