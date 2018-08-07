# -*- coding: utf-8 -*-
# Модуль для проверки есть ли файл в папке

import os

# Год, месяц и наименование ЛПУ для файла в архиве
# year, month, glpu
def exist(dir, year, month, glpu):

    #Наименование файла zip c xml
    file_zip = 'HT05S50_' + year[2:4] + month + glpu

    if os.path.exists(dir + file_zip + 'P.ZIP'):
        return dir + file_zip + 'P.ZIP'
    elif os.path.exists(dir + file_zip + 'O.ZIP'):
        return dir + file_zip + 'O.ZIP'
    else:
        # Если файла нет то ошибка
        return False