import telebot
import time
from telebot import types

bot = telebot.TeleBot('6060902050:AAE9IZks_wK6YQjZYwebjqaruDA_jXEWisE')


class Kachok:
    """class for all club members"""
    # alias and name enough to initialize member, other information can be added later
    def __init__(self, alias, name):
        # If name include * at the end this member is female
        # Since there are very few women in the club, this is more convenient than adding methods
        if name[-1] == '*':
            self.female = True
            self.name = name[0, -1]
        else:
            self.female = False
            self.name = name

        # Telegram alias of club member
        self.alias = alias
        # Member's current self weight
        self.selfWeight = 100
        # Member's max weight
        self.weight = 0
        # Member's max points
        self.proteinPoints = 0
        # Member's best grade
        self.mark = "(D)"
        # Dictionary of points in format date:points
        self.proteinPointsByDate = {}
        # Dictionary of weights in format date:points
        self.weightByDate = {}

    def make_female(self):
        """function that can be helpful if * forgotten while adding female member"""
        if not self.female:
            self.proteinPoints *= 1.64
            for i in self.proteinPointsByDate:
                self.proteinPointsByDate[i] *= 1.64
        self.female = True
        self.grade()

    def grade(self):
        """function that update member grade"""
        if self.proteinPoints < 0.8:
            self.mark = "(D)"
        elif self.proteinPoints < 1:
            self.mark = "(C)"
        elif self.proteinPoints < 1.2:
            self.mark = "(B)"
        else:
            self.mark = "(A)"

    def set_self_weight(self, weight):
        """function that update member self weight"""
        # since new self weight not taken into account for previous results not so many actions needed
        self.selfWeight = float(weight)

    def set_weight(self, weight):
        """function that update member weight"""
        # Member's max weight updates if needed
        self.weight = max(float(weight), self.weight)
        # Member's max points updates if needed
        if self.female:
            self.proteinPoints = max(self.proteinPoints, float(weight)*1.64 / self.selfWeight)
        else:
            self.proteinPoints = max(self.proteinPoints, float(weight)/self.selfWeight)
        # the current date is taken
        date = time.strftime("%d/%m/%Y")
        if date not in self.weightByDate:
            self.weightByDate[date] = float(weight)
            self.proteinPointsByDate[date] = float(weight) / self.selfWeight
            if self.female:
                self.proteinPointsByDate[date] *= 1.64
        else:
            self.weightByDate[date] = max(float(weight), self.weightByDate[date])
            if not self.female:
                if float(weight) / self.selfWeight > self.proteinPointsByDate[date]:
                    self.proteinPointsByDate[date] = float(weight) / self.selfWeight
            else:
                if float(weight) * 1.64 / self.selfWeight > self.proteinPointsByDate[date]:
                    self.proteinPointsByDate[date] = float(weight) * 1.64 / self.selfWeight
        self.grade()

    def set_name(self, name):
        """function that change member name"""
        self.name = name

    def display(self):
        """function that display necessary information about member, using in displaying top"""
        information_1 = self.name + ' ' + self.alias + ' - ' + str(int(self.weight)) + ' kg - '
        information_2 = str(int(self.proteinPoints * 100)) + ' PP ' + self.mark
        information = information_1 + information_2
        return information

    
# static text for sending to user
greet = '! Добро пожаловать в innoтягу! \n Для того чтобы вывести доступные команды чиркани /help. \n ' \
        'Для того чтобы вывести топ участников за всё время напиши /top.\n '
schedule_ = 'Занятия иннотяги проходят в 19:00 по средам, пятницам и воскресеньям \n ' \
            'Среда - спина и бицепс, пятниа - ноги, воскресенье - трицепс и грудь' \
           'также иногда проводяться дополнительные занятия, ' \
           'информацию по которым можно найти в основной беседе клуба: @innotyaga'
pp = 'Количество полученных протеин поинтов - ' \
     'вес который ты поднял умноженный на 100 и поделённый на твой собсвенный вес. ' \
     'Для девушек полученное количество умножается на 1.64. \n Цешка начинается с 80, бэшка со 100 и ашка со 120'
empty = 'Я понимаю только определённые команды. Попробуй написать /start'
newMemberSuccess = 'Участник добавлен успешно'
newMemberFail = 'Такой участник уже зарегестрирован'
emptyTop = "No members in top now. You can add members to top using /olduser or /newuser commands. " \
           "Type /help for more information. "
goodPhoto = 'Неплохое фото. Ставлю 8.5 из 10.'
regProblem = 'У вас какие то проблемы с именем или алиасом. Попросите @kupamonke вас зарегистрировать'
commands = '/start - начать \n /help - посмотреть список всех возможный команд \n' \
            '/schedule - взглянуть на расписание занятий. ' \
            '/pp - правила получения протеин поинтов и оценок \n' \
            '/top - отобразить топ участников по жиму штанги от груди \n' \
            '/register - зарегистрироваться в боте. В результате ваши имя и алиас добавяться в топ \n' \
            '/newuser - добавить нового участника. В результате чужие имя и алиас появяться в боте. \n' \
            '/olduser - добавить участника которого взвешивали и который уже пожал. ' \
            'В результате его результаты появяться в топе. \n' \
            '/setweight - поменять вес который учасник смог пожать. \n' \
            '/setselfweight - поменять вес который учасник смог пожать.\n'\
            '/changename - поменять имя участника. \n' \
            '/makefemale - сделать участника женщиной. \n' \
            '/delete - удалить участника из топа \n' \
            '/DanilNikulin - Данил Никулин.'
nikulin = '/DanilNikulin'
enter_alias = 'введите алиас участника'

notInVip = 'У вас нет доступа к этой команде. Если вы считаете что произошла ошибка напишите @kupamonke'

# list of alias of members who have access to all commands
vip_members = ["kupamonke", "ez4gotit", 'elonnmax228', 'realbean', 'justdanman', 'prettygoodtechguy']

# dictionary that remember information in format user_chat_id:information
# used in functions with register_next_step_handler
user_dict = {}


# dictionary of all members in alias:Kachok format, sorted after any changes
w = {}  # This should be your Kachok dictionary


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


def do_some_sorting(members):
    """function that sort dictionary by protein points of values, used for sort top"""
    members = dict(sorted(members.items(), key=lambda item: item[1].proteinPoints, reverse=True))
    return members


@bot.message_handler(commands=['top'])
def top(user):
    """function that display top"""
    global w
    c = 0
    s = ""
    # display all members
    for i in w:
        c += 1
        s += str(c) + " " + w.get(i).display() + '\n'
    # in case top empty send message indicating about
    if s == '':
        bot.send_message(user.chat.id, emptyTop)
    else:
        bot.send_message(user.chat.id, s)


@bot.message_handler(commands=['register'])
def register(user):
    """function that add to top member who send "/register" message"""
    global w
    try:
        # function takes alias and name of user who send this command
        alias = user.from_user.username
        alias = '@' + alias
        alias = alias.lower()
        name = user.from_user.first_name
        # add user to top and sort it
        if alias not in w:
            member = Kachok(alias, name)
            w[alias] = member
            bot.send_message(user.chat.id, newMemberSuccess)
            w = do_some_sorting(w)
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
    global w
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
    global w
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
        if alias not in w:
            member = Kachok(alias, name)
            member.set_self_weight(self_weight)
            member.set_weight(weight)
            w[alias] = member
            bot.send_message(user.chat.id, newMemberSuccess)
            w = do_some_sorting(w)
        else:
            bot.send_message(user.chat.id, newMemberFail)

    except Exception:
        bot.send_message(user.chat.id, 'Что-то пошло не так. Попробуй ещё разок.')
    user_dict[user.chat.id] = ''


@bot.message_handler(commands=['changename'])
def changename(user):
    """function that change member name"""
    # only several users can use this command
    global w
    if user.from_user.username.lower() not in vip_members:
        bot.send_message(user.chat.id, notInVip)
        return 0
    global w
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in w:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, changename_answer)


def changename_answer(user):
    global w
    if user.text not in w:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    msg = bot.reply_to(user, 'введите новое имя участника', reply_markup=rmk)
    bot.register_next_step_handler(msg, changename_answer_2)


def changename_answer_2(user):
    global w
    user_dict[user.chat.id] += ' ' + user.text
    try:
        alias, name = user_dict[user.chat.id].split()
        alias = alias.lower()
        if alias not in w:
            bot.send_message(user.chat.id, 'Участник не найден')
        else:
            w.get(alias).set_name(name)
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
    global w
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in w:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, makefemale_answer)


def makefemale_answer(user):
    global w
    if user.text not in w:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(user, 'Делаем из участника женшину...', reply_markup=rmk)
    try:
        alias = user_dict[user.chat.id]
        if alias not in w:
            bot.send_message(user.chat.id, 'Участник не найден')
        else:
            w.get(alias).make_female()
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
    global w
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in w:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, setweight_answer)


def setweight_answer(user):
    global w
    if user.text not in w:
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
    global w
    try:
        alias = user_dict[user.chat.id]
        w.get(alias).set_weight(user.text)
        w = do_some_sorting(w)
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
    global w
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in w:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, setselfweight_answer)


def setselfweight_answer(user):
    global w
    if user.text not in w:
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
    global w
    try:
        alias = user_dict[user.chat.id]
        w.get(alias).set_self_weight(user.text)
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
    global w
    try:
        alias = user_dict[user.chat.id]
        member = Kachok(alias, user.text)
        w[alias] = member
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
    global w
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in w:
        rmk.add(i)
    msg = bot.reply_to(user, enter_alias, reply_markup=rmk)
    bot.register_next_step_handler(msg, delete_answer)


def delete_answer(user):
    global w
    if user.text not in w:
        bot.send_message(user.chat.id, 'Этот участник не зареган, попробуй ещё разок')
        return 0
    user_dict[user.chat.id] = user.text
    rmk = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(user, 'Делаем из участника женшину...', reply_markup=rmk)
    try:
        alias = user_dict[user.chat.id]
        if alias not in w:
            bot.send_message(user.chat.id, 'Участник не найден')
        else:
            w.get(alias).make_female()
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
    global w
    w = do_some_sorting(w)


@bot.message_handler()
def wrong_command(user):
    """function that send to user information that such command did not exist"""
    bot.send_message(user.chat.id, empty)


@bot.message_handler(content_types=['photo'])
def photo(user):
    """function that handles photos"""
    bot.reply_to(user, goodPhoto)


bot.polling(none_stop=True)

