# -*- coding: utf-8 -*-

intervals = (
    # ('час', 3600),    # 60 * 60
    ('мин', 60),
    ('сек', 1),
    )

def display_time(seconds):
    x = str(seconds).find('.')
    sec = str(seconds)[x+1:x+3]
    result = []

    for name, count in intervals:
        value = seconds // count
        seconds -= value * count
        if name == 'сек':
            result.append(f"{int(value)}.{sec} {name}")
        else:
            result.append(f"{int(value)} {name}")

    return ', '.join(result)