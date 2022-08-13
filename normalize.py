import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                 "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    try:
        name = name.translate(TRANS)
        name = re.sub(r'[^\w|.]', '_', name)
        return name
    except AttributeError:
        return print("data should be a string")