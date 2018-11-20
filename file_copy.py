# -*- coding: utf-8 -*-

import shutil
import os


def mcopy(file_from, file_to):
    try:
        if os.path.isfile(file_from):
            #and os.access(file_from, os.R_OK
            try:
                shutil.copy(file_from, file_to)
                os.remove(file_from)
            except OSError as e:
                print(f'Error copy files: {e.filename} - {e.strerror}.')
    except IOError as err:
        print(err)
