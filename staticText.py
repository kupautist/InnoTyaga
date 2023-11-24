# static text for sending to user
class RU:
    enter_new_alias = 'Заебись'
    greet = '! Добро пожаловать в innoтягу!\n Для того чтобы вывести доступные команды чиркани /help.\n' \
            'Для того чтобы вывести топ участников за всё время напишите /top.\n' \
            'Чтобы учавствовать в топе, необходимо зарегистрироваться: /register.\n'
    schedule_ = 'Занятия иннотяги проходят в 19:00 по средам, пятницам и воскресеньям\n' \
                'Среда - спина и бицепс, пятниа - ноги, воскресенье - трицепс и грудь\n' \
                'Также иногда проводяться дополнительные занятия, ' \
                'информацию по которым можно найти в основной беседе клуба: @innotyaga'
    pp = 'Количество полученных протеин поинтов - ' \
         'вес который вы подняли умноженный на 100 и поделённый на ваш собсвенный вес. ' \
         'Для девушек полученное количество умножается на 1.64.\nЦешка начинается с 80, бэшка со 100 и ашка со 120'
    empty = 'Я понимаю только определённые команды. Попробуй написать /help'
    newMemberSuccess = 'Участник добавлен успешно'
    newMemberFail = 'Такой участник уже зарегестрирован'
    emptyTop = "No members in top now.\nYou can add members to top using /olduser or /newuser commands." \
               "Type /help for more information. "
    goodPhoto = 'Неплохое фото. Ставлю 8.5 из 10.'
    regProblem = 'У вас какие то проблемы с именем или алиасом. Попросите @kupamonke вас зарегистрировать'
    commands = ['/start - начать\n''/help - посмотреть список всех возможный команд\n''/register - зарегистрироваться в боте. В результате ваши имя и алиас добавяться в топ\n''/top - отобразить топ участников по жиму штанги от груди\n''/schedule - взглянуть на расписание занятий.\n''/pp - правила получения протеин поинтов и оценок\n''/info - отобразить ваш профиль и историю жима\n''/DanilNikulin - кто такой Данил Никулин?\n'
        ,
                'Доступ к следующим командам есть только у самых гейских геев иннотяги\n\n''/newuser - добавить нового участника. В результате чужие имя и алиас появяться в боте.\n''/olduser - добавить участника которого взвешивали, и который уже пожал. ''В результате его результаты появяться в топе.\n''/setweight - поменять вес который учасник смог пожать.\n''/setselfweight - поменять личный вес участника.\n''/changename - поменять имя участника.\n''/makefemale - сделать участника женщиной.\n''/delete - удалить участника из топа\n'
        ,
                'Доступ к этим командам есть только у владельцев клуба\n\n''/reload - загрузить данные с базы\n'
                '/chaccess - изменить уровень доступа участника'
                ]
    nikulin = '/DanilNikulin'
    enter_alias = 'Введите алиас участника'
    enter_name = 'Введите имя участника'
    enter_self_weight = 'Введите вес участника'
    enter_weight = 'введите вес который участник смог пожать'
    not_registered = 'Этот участник не зареган, попробуй ещё разок'
    accessDenied = 'У вас нет доступа к этой команде. Если вы считаете что произошла ошибка напишите @kupamonke'
    deleting = 'Удаляем участника...'
    success = 'Успешно'
    exception = 'Что-то пошло не так'
    weight_format = 'Введите вес в формате 61.5. Запятые, символы и прочая херня запрещена.'
    making_woman = 'Делаем из участника женшину...'
    no_spaces = 'Пробелы - непозволительная роскошь.\n Попробуй ещё раз.'
    long_name = 'Имя слишом длинное, ограничься 16 символами.\n Попробуй ещё раз.'
    reg = 'Вы не зарегестрированны, исправить это можно командой /register'
