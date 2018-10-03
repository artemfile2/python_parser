# -*- coding: utf-8 -*-

import timeit
from time import strftime, localtime, sleep

from PyQt5.QtWidgets import QApplication

from file_exist import *
from file_extract import *
from file_copy import *
from xml_todb import *
from connect import *
from msectohmc import display_time


def check_table(period):
    """
        Функция проверки есть ли данные в таблице
    """

    # //TODO: сделать проверку секции и при необходимости создавать новые
    try:
        db = con('db')
        dbcur = db.cursor()
        # queryCheck = """SELECT TABLE_NAME FROM ALL_TABLES WHERE UPPER(TABLE_NAME) = UPPER(:name_table)"""
        queryCheck = """SELECT SCHET WHERE period = :period"""
        dbcur.execute(queryCheck, (period,))
        table_check = dbcur.fetchone()
        if table_check is None:
            return False
        else:
            return True
    except cx_Oracle.Error as err:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Query error: {}".format(err))
        msg.setWindowTitle("Ошибка в запросе")
        msg.setDetailedText("Query error: {}".format(err))
        msg.exec_()
        print("Query error: {}".format(err))


def extractZipXml(self, year, month, dir_XmlZip, tmp):
    """
    Функция работы с архивом
    """
    #check_table('ST05S50' + year + month):

    self.ui.textEdit.append('Данные за отчетный период ' + year + ' ' + month + ' с XML загружаются...')
    QApplication.instance().processEvents()

    i_infinity = 0
    while i_infinity < 10:

        slpu = get_glpu()

        for lpu in slpu:
            glpu = lpu[0]
            name_mo = lpu[3]

            if exist(dir_XmlZip, year, month, glpu):
                print(dir_XmlZip + glpu +' '+ month + year)
                time_start = timeit.default_timer()
                # Получаю файл ZIP из папки VipNet
                pathfile_zip = exist(dir_XmlZip, year, month, glpu)
                sleep(1)
                # Копирую архив во временную папку
                copy(pathfile_zip, tmp)
                # Получаю новый путь из временной папки
                tmp_zip = exist(tmp, year, month, glpu)
                self.ui.textEdit.append(tmp_zip )
                QApplication.instance().processEvents()

                # Извлекаю из архива файлы и удаляю архив = True
                extract(tmp_zip, tmp, True)
                get_file_xml(tmp_zip, year, month, glpu)
                tm_wr = str(timeit.default_timer() - time_start)
                tm_wr2 = timeit.default_timer() - time_start
                tt = display_time(tm_wr2)
                print(tmp_zip + ' ' + name_mo.strip() + ' время обработки: ' + tm_wr[0: 5])

                self.ui.textEdit.append('  ==> ' + name_mo.strip() + '\n' +
                                        '  ==> дата/время: ' + strftime("%d.%m.%Y %H:%M:%S", localtime()) + '\n' +
                                        '  ==> время обработки: ' + tt + '\n')
                QApplication.instance().processEvents()