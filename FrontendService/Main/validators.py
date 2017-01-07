from django.core.exceptions import ValidationError
import unicodedata as ud


def validate_cyrillic(value):
    # latin_letters = {}
    # cyrillic = {'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщыъьэюя'}
    #
    # def is_latin(uchr):
    #     try:
    #         return latin_letters[uchr]
    #     except KeyError:
    #         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))
    #
    # def romanstr(unistr):
    #     return all(is_latin(uchr)
    #                for uchr in unistr
    #                if uchr not in cyrillic)  # isalpha suggested by John Machin
    def romanstr(unistr):
        for x in unistr:
            string = ud.name(x)
            if 'CYRILLIC' in string:
                return False
        return True

    if not romanstr(value):
        return False
    else:
        return True

