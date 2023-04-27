import time


def convert_month(month_s):
    month = month_s.lower()

    if convert_int(month) is not None:
        return convert_int(month)

    if convert_abbr(month) is not None:
        return convert_abbr(month)

    if convert_month_english(month) is not None:
        return convert_month_english(month)

    if convert_abbr_fr(month) is not None:
        return convert_abbr_fr(month)

    if convert_long_fr(month) is not None:
        return convert_long_fr(month)


def convert_int(int_s):
    try:
        return int(int_s)
    except ValueError:
        return None


def convert_abbr(month_s):
    try:
        return time.strptime(month_s, '%b').tm_mon
    except ValueError:
        return None


def convert_month_english(month_s):
    try:
        return time.strptime(month_s, '%B').tm_mon
    except ValueError:
        return None


def convert_abbr_fr(month_s):
    return {
        'janv': 1,
        'févr': 2,
        'mars': 3,
        'avr': 4,
        'mai': 5,
        'juin': 6,
        'juil': 7,
        'août': 8,
        'sept': 9,
        'oct': 10,
        'nov': 11,
        'déc': 12
    }.get(month_s)


def convert_long_fr(month_s):
    return {
        'janvier': 1,
        'février': 2,
        'mars': 3,
        'avril': 4,
        'mai': 5,
        'juin': 6,
        'juillet': 7,
        'août': 8,
        'septembre': 9,
        'octobre': 10,
        'novembre': 11,
        'décembre': 12
    }.get(month_s)
