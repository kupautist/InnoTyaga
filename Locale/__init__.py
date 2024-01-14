import logging
from Locale.LocaleBase import Locale
from Locale.LocaleRu import LocaleRU
from Locale.LocaleEn import LocaleEN
from telebot.types import Message
__locale_classes = [LocaleRU, LocaleEN]


def get_locale(code: str | Message) -> type[Locale]:
    if isinstance(code, Message):
        code = code.from_user.language_code
    match code:
        case 'en':
            return LocaleEN
        case 'ru':
            return LocaleRU
        case _:
            return LocaleRU


def __check_lang_string_class(other: type[Locale]) -> list[str]:
    result = []
    for k in Locale.__dict__:
        if not k.startswith('__') and ((k not in other.__dict__.keys()) or (other.__dict__[k] in ('', ['']))):
            result.append(f'{other.__name__} has no {k} field.')
    return result


def __check_lang_string_classes() -> None:
    locale_errors = [item for list in [__check_lang_string_class(
        i) for i in __locale_classes] for item in list]
    if locale_errors:
        logging.error('\n'.join(locale_errors))


__check_lang_string_classes()
