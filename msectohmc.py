# -*- coding: utf-8 -*-

intervals = (
    ('час', 3600),    # 60 * 60
    ('мин', 60),
    ('сек', 1),
    )

def display_time(seconds, granularity=3):
    result = []

    for name, count in intervals:
        value = seconds // count
        seconds -= value * count
        result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])