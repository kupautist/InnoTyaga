from telebot import types
from kachok import Kachok
from staticText import *
from botInstance import bot
from data import kachki, user_dict, vip_members, updateRecords

@bot.message_handler(commands=['start', 'начать'])
def start(user):
    """function that greets the user"""
    bot.send_message(user.chat.id, f'Здарова, {user.from_user.first_name} {user.from_user.last_name}' + greet)


@bot.message_handler(commands=['help', 'помощь'])
def commands_list(user):
    """function that send to user list of possible commands and their description"""
    bot.send_message(user.chat.id, commands)


@bot.message_handler(commands=['schedule'])
def schedule(user):
    """function that send to user schedule of club meetings"""
    bot.send_message(user.chat.id, schedule_)


@bot.message_handler(commands=['pp'])
def grading(user):
    """function that send to user grading information"""
    bot.send_message(user.chat.id, pp)


@bot.message_handler(commands=['top'])
def top(user):
    """function that display top"""
    global kachki
    c = 0
    s = ""
    # display all members
    for i in kachki:
        c += 1
        s += str(c) + " " + kachki.get(i).display() + '\n'
    # in case top empty send message indicating about
    if s == '':
        bot.send_message(user.chat.id, emptyTop)
    else:
        bot.send_message(user.chat.id, s)


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
    except Exception:
        bot.send_message(user.chat.id, regProblem)


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
    # member's alias saved
    if user.text[0] != '@':
        user_dict[user.chat.id] = '@' + user.text
    else:
        user_dict[user.chat.id] = user.text
    # member's name requested
    msg = bot.reply_to(user, 'введите имя участника (одно слово)')
    bot.register_next_step_handler(msg, olduser_answer_2)


def olduser_answer_2(user):
    """part 3 of function that add to top old member"""
    # check if name to include space
    for i in user.text:
        if ord(i) == 32:
            msg = bot.reply_to(user, 'Пробелы - непозволительная роскошь.\n Попробуй ещё раз.')
            bot.register_next_step_handler(msg, olduser_answer_2)
            return 0
    # check if name to long
    if len(user.text) > 16:
        msg = bot.reply_to(user, 'Имя слишом длинное, ограничься 16 символами.\n Попробуй ещё раз.')
        bot.register_next_step_handler(msg, olduser_answer_2)
        return 0
    # member's name saved
    user_dict[user.chat.id] += ' ' + user.text
    # member's self weight requested
    msg = bot.reply_to(user, 'введите вес участника')
    bot.register_next_step_handler(msg, olduser_answer_3)


def olduser_answer_3(user):
    """part 4 of function that add to top old member"""
    # check if self weight format incorrect
    try:
        float(user.text)
    except ValueError:
        msg = bot.send_message(user.chat.id, 'Введите вес в формате 63.45. Запятые, символы и прочая херня запрещена.')
        bot.register_next_step_handler(msg, olduser_answer_3)
        return 0
    # member's self weight saved
    user_dict[user.chat.id] += ' ' + user.text
    # member's weight requested
    msg = bot.reply_to(user, 'введите вес который участник пожал')
    bot.register_next_step_handler(msg, olduser_answer_4)


def olduser_answer_4(user):
    """part 5 of function that add to top old member"""
    global kachki
    # check if weight format incorrect
    try:
        float(user.text)
    except ValueError:
        msg = bot.send_message(user.chat.id, 'Введите вес в формате 61.5. Запятые, символы и прочая херня запрещена.')
        bot.register_next_step_handler(msg, olduser_answer_4)
        return 0
    # member's weight saved
    user_dict[user.chat.id] += ' ' + user.text
    try:
        alias, name, self_weight, weight = user_dict[user.chat.id].split()
        alias = alias.lower()
        if alias not in kachki:
            member = Kachok(alias, name)
            member.set_self_weight(self_weight)
            member.set_weight(weight)
            kachki[alias] = member
            bot.send_message(user.chat.id, newMemberSuccess)
            updateRecords()
        else:
            bot.send_message(user.chat.id, newMemberFail)

    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так. Попробуй ещё разок.')
    user_dict[user.chat.id] = ''


@bot.message_handler(commands=['changename'])
def changename(user):
    """function that change member name"""
    # only several users can use this command
    global kachki
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, changename_answer)


def changename_answer(user):
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    msg = bot.reply_to(user, 'введите новое имя участника', reply_markup=rmk)
    bot.register_next_step_handler(msg, changename_answer_2)


def changename_answer_2(user):
    global kachki
    user_dict[user.chat.id] += ' ' + user.text
    try:
        alias, name = user_dict[user.chat.id].split()
        alias = alias.lower()
        if alias not in kachki:
            bot.send_message(user.chat.id, 'Участник не найден')
        else:
            kachki.get(alias).set_name(name)
            bot.send_message(user.chat.id, 'Успешно')
    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так. \nКто такой Данил Никулин??')
    user_dict[user.chat.id] = ''


@bot.message_handler(commands=['makefemale'])
def makefemale(user):
    """function that can be helpful if * forgotten while adding female member"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, makefemale_answer)


def makefemale_answer(user):
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(user, 'Делаем из участника женшину...', reply_markup=rmk)
    try:
        alias = user_dict[user.chat.id]
        if alias not in kachki:
            bot.send_message(user.chat.id, 'Участник не найден')
        else:
            kachki.get(alias).make_female()
            bot.send_message(user.chat.id, 'Успешно')
    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так')
    user_dict[user.chat.id] = ''


@bot.message_handler(commands=['setweight'])
def set_weight(user):
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, setweight_answer)


def setweight_answer(user):
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    msg = bot.reply_to(user, 'введите вес который участник смог пожать', reply_markup=rmk)
    bot.register_next_step_handler(msg, setweight_answer_2)


def setweight_answer_2(user):
    try:
        float(user.text)
    except ValueError:
        msg = bot.send_message(user.chat.id, 'Введите вес в формате 61.5. Запятые, символы и прочая херня запрещена.')
        bot.register_next_step_handler(msg, olduser_answer_4)
        return 0
    global kachki
    try:
        alias = user_dict[user.chat.id]
        kachki.get(alias).set_weight(user.text)
        updateRecords()
        bot.send_message(user.chat.id, 'Успешно')
    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так')
    user_dict[user.chat.id] = ''


@bot.message_handler(commands=['setselfweight'])
def set_self_weight(user):
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer)


def setselfweight_answer(user):
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    msg = bot.reply_to(user, 'введите вес участника', reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer_2)


def setselfweight_answer_2(user):
    try:
        float(user.text)
    except ValueError:
        msg = bot.send_message(user.chat.id, 'Введите вес в формате 61.5. Запятые, символы и прочая херня запрещена.')
        bot.register_next_step_handler(msg, olduser_answer_4)
        return 0
    global kachki
    try:
        alias = user_dict[user.chat.id]
        kachki.get(alias).set_self_weight(user.text)
        bot.send_message(user.chat.id, 'Успешно')
    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так')
    user_dict[user.chat.id] = ''


@bot.message_handler(commands=['newuser'])
def new_user(user):
    """function that add to top new member"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    msg = bot.reply_to(user, enter_alias)
    bot.register_next_step_handler(msg, new_user_answer)


def new_user_answer(user):
    if user.text[0] != '@':
        user_dict[user.chat.id] = '@' + user.text
    else:
        user_dict[user.chat.id] = user.text
    msg = bot.reply_to(user, 'введите имя участника')
    bot.register_next_step_handler(msg, new_user_answer_2)


def new_user_answer_2(user):
    global kachki
    try:
        alias = user_dict[user.chat.id]
        member = Kachok(alias, user.text)
        kachki[alias] = member
        bot.send_message(user.chat.id, 'Успешно')
        user_dict[user.chat.id] = ''
    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['delete'])
def delete_nikulin(user):
    """function for deleting member from top"""
    # only several users can use this command
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    global kachki
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in kachki:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, delete_answer)


def delete_answer(user):
    global kachki
    if user.text not in kachki:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(user, 'Делаем из участника женшину...', reply_markup=rmk)
    try:
        alias = user_dict[user.chat.id]
        if alias not in kachki:
            bot.send_message(user.chat.id, 'Участник не найден')
        else:
            kachki.get(alias).make_female()
            bot.send_message(user.chat.id, 'Успешно')
    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так')
    user_dict[user.chat.id] = ''


@bot.message_handler(commands=['danilnikulin', 'DanilNikulin'])
def danil_nikulin(user):
    """DanilNikulin"""
    for i in range(10):
        bot.send_message(user.chat.id, nikulin)


@bot.message_handler(commands=['sort'])
def sort_nikulin(user):
    """function that able to call do_some_sorting from telegram"""
    global kachki
    updateRecords()


@bot.message_handler()
def wrong_command(user):
    """function that send to user information that such command did not exist"""
    bot.send_message(user.chat.id, empty)


@bot.message_handler(content_types=['photo'])
def photo(user):
    """function that handles photos"""
    bot.reply_to(user, goodPhoto)
