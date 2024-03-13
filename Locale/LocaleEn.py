from dataclasses import dataclass
from Locale.LocaleBase import Locale


@dataclass(frozen=True)
class LocaleEN(Locale):
    greet = ['Howdy',
             '! Welcome to the InnoTyaga!\n'
             'To display available commands, type /help.\n'
             'To display all-time top participants, write /top.\n'
             'To participate in the top, you need to register: /register.\n'
             ]
    schedule = 'Да похуй всем Серёжа Допизделся\\) Лучше выложи расклад карт таро на твою ' \
        'ЛЕГЕНДАРНЕЙШЕЮ "Прошедшей ночью данные ребята ломились не в свою квартиру в 130 доме. ' \
        'При вопросе "чонада" свалили в закат. Наверное дом перепутали. Или город. ' \
        'Короче скоро новый год и иронию судьбы косплеели ребята...надеюсь...\n' \
        'Говорят местные перепутали 130 и 114 дом." в Иннополисе мы все ждем\n\n'  \
        '*Info on the ever-changing class schedule subscribe to the official info channel @innotyaga*'
    pp = 'The number of protein points received is the weight you lifted multiplied by 100' \
        'and divided by your own weight. For females, the number is multiplied by 1.64.\n' \
        'C starts at 80, B at 100 and A at 120.'
    command_unknown = 'I only understand certain commands. Try typing /help'
    newMemberSuccess = 'Member added successfully'
    alreadyRegistred = 'This member is already registered'
    emptyTop = 'No members in the top now.\nYou can add members to the top using /olduser or /newuser commands.\n' \
        'Type /help for more information.'
    goodPhoto = 'Quite a photo. I give it 8.5 out of 10.'
    regProblem = 'You have some kind of problem with your name or alias. Ask @kupamonke to register you'
    commands = ["/start - start\n"
                "/help - see the list of all possible commands\n"
                "/register - register in the bot. As a result, your name and alias will be added to the top.\n"
                "/top - display the top of participants\n"
                "/schedule - see the schedule of the training sessions.\n"
                "/pp - rules for protein points and grading\n"
                "/info - display your profile and your barbell bench press history\n"
                "/DanilNikulin - who is Danil Nikulin?",
                "_*Only the gayest gays of InnoTyaga have access to the following commands*_\n\n"
                "/newuser - add a new member. As a result, the specified name and alias will appear in the bot.\n"
                "/olduser - add a member who was weighed and who has already lifted."
                "As a result, their results will appear in the top.\n"
                "/setweight - set the weight that the participant was able to lift.\n"
                "/setselfweight - change a member's self weight.\n"
                "/changename - change the name of the member.\n"
                "/makefemale - turn the member into a woman.\n"
                "/delete - remove the member from the top.",
                "_*Only club owners have access to these commands*_\n\n"
                "/reload - load data from the database\n"
                "/stop - stops current running instance of a bot\n"
                "/chaccess - change access level of a member"
                ]
    nikulin = '/DanilNikulin'
    enter_alias = "Enter the member's alias"
    enter_name = "Enter the name of the member"
    enter_self_weight = "Enter the member's weight"
    enter_weight = "Enter the weight that the participant was able to lift"
    not_registered = 'This member is not registered, try again.'
    accessDenied = "You do not have access to this command. If you think there's been an error, ask @kupamonke"
    deleting = 'Removing member...'
    success = 'Success'
    exception = 'Something went wrong'
    weight_format = "Enter weight in the format 61.5. Commas, symbols and other bullshit are not allowed."
    making_woman = 'Turning the member into a woman...'
    long_name = 'The name is too long, limit it to 16 characters.\nTry again.'
    reg = "You are not registered, but you can fix it with the command /register"
    personal_best = "Personal Best"
    no_weight = "You haven't lifted anything yet. At least lift an empty barbell (20kg), I believe in you!!!"
    info_history = ["you lifted", "and got"]