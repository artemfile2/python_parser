# -*- coding: utf-8 -*-

import shutil
import os

def copy(file_from, file_to):
    try:
        if os.path.isfile(file_from): #and os.access(file_from, os.R_OK
            shutil.copy(file_from, file_to)
            os.remove(file_from)
    except IOError as err:
        print(err)