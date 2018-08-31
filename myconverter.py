# -*- coding: utf-8 -*-

def convert_none_type(obj):
    """
        функция проверки поля в XML
        если поля нет или NUll то
        чтобы ошибки не было возвращаю пустую строку
        :type obj: object
    """
    try:
        if obj is None:
            return ''
        else:
            if obj.text is None:
                return ''
            else:
                return obj.text
    except TypeError:
        return ''