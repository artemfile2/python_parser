from file_exist import *
from file_extract import *
from file_copy import *
import timeit
from time import strftime, localtime, sleep
from xml_todb import *
from connect import *
from PyQt5.QtWidgets import QApplication

"""
Функция работы с архивом
"""
def extractZipXml(self, year, month, dir_XmlZip, tmp):

    i_infinity = 0
    while i_infinity < 10:

        slpu = get_glpu()

        for lpu in slpu:
            glpu = lpu[0]
            name_mo = lpu[3] #get_slpuonglpu(glpu)

            # time_start = timeit.default_timer()
            if exist(dir_XmlZip, year, month, glpu):
                time_start = timeit.default_timer()
                #Получаю файл ZIP из папки VipNet
                pathfile_zip = exist(dir_XmlZip, year, month, glpu)
                #Копирую архив во временную папку
                copy(pathfile_zip, tmp)
                sleep(1)
                #Получаю новый путь из временной папки
                tmp_zip = exist(tmp, year, month, glpu)
                #Извлекаю из архива файлы и удаляю архив = True
                extract(tmp_zip, tmp, True)
                getFileXml(tmp_zip, year, month, glpu)
                tm_wr = str(timeit.default_timer() - time_start)
                print(tmp_zip + ' ' + name_mo.strip() + ' время обработки: ' + tm_wr[0: 5])

                self.ui.textEdit.append(tmp_zip + '\n' +
                                        '  ==> ' + name_mo.strip() + '\n' +
                                        '  ==> дата/время: ' + strftime("%d.%m.%Y %H:%M:%S", localtime()) + '\n' +
                                        '  ==> время обработки: ' + tm_wr[0: 5] + '\n')
                QApplication.instance().processEvents()