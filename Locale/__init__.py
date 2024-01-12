import logging
from LocaleBase import *
from LocaleRU import *
from telebot.types import Message

def get_locale(code: str) -> type[Locale]:
    match code:
        case 'ru':
            return LocaleRU
        case _:
            return LocaleRU

def get_locale(msg: Message) -> type[Locale]:
    return get_locale(msg.from_user.language_code)

def __check_lang_string_class(other: type[Locale]) -> list[str]:
    result = []
    for k in Locale.__dict__:
        if not k.startswith('__') and ((k not in other.__dict__) or other.__dict__[k] == ''):
            result.append(f'{other.__name__} has no {k} field.')
    return result

__locale_classes = [LocaleRU]

def __check_lang_string_classes() -> None:
    locale_errors = [item for list in [__check_lang_string_class(i) for i in __locale_classes] for item in list]
    if locale_errors:
        logging.error('\n'.join(locale_errors))

__check_lang_string_classes()