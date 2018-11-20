# -*- coding: utf-8 -*-
# Модуль для извлечения файлов из ZIP архива

import zipfile
import os


def extract(zippedFile, toFolder, delete=False):
    if os.path.isfile(zippedFile):
        #and os.access(zippedFile, os.R_OK)
        with zipfile.ZipFile(zippedFile, 'r') as zfile:
            try:
                zfile.extractall(path=toFolder)
                zfile.close()
                if delete:
                    os.remove(zippedFile)
            except IOError as err:
                print(err)
