from .parser import entries


def parse(text):
    return entries.parse_string(text, True)[0]
