# -*- coding: utf-8 -*-

import timeit
from time import strftime, localtime, sleep

from PyQt5.QtWidgets import QApplication

from file_exist import *
from file_extract import *
from file_copy import *
from xml_todb import *
from connect import *
import msectohmc


def create_tables(period):
    """
        Функция создания таблиц
    """
    try:
        db = con('db')
        dbcur = db.cursor()
        dbcur.execute(f"CALL SYSTEM.CREATE_TABLE('{period}')")
        db.commit()
        dbcur.close()

    except cx_Oracle.Error as err:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(f"Query error: {err}")
        msg.setWindowTitle("Ошибка в запросе CREATE_TABLE")
        msg.setDetailedText(f"Query error CREATE_TABLE: {err}")
        msg.exec_()
        print(f"Query error: {err}")


def check_table(name_table):
    """
        Функция проверки есть ли такие таблицы
    """
    try:
        db = con('db')
        dbcur = db.cursor()
        # queryCheck = """SELECT TABLE_NAME FROM ALL_TABLES WHERE UPPER(TABLE_NAME) = UPPER({!r})""".format(name_table)
        queryCheck = """SELECT TABLE_NAME FROM ALL_TABLES WHERE UPPER(TABLE_NAME) = UPPER(:name_table)"""
        dbcur.execute(queryCheck, (name_table,))
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
    if check_table('ST05S50' + year + month):
        self.ui.textEdit.append('Таблицы за отчетный период ' + year + ' ' + month +
                                ' найдены, данные с XML загружаются...')
        QApplication.instance().processEvents()
    else:
        self.ui.textEdit.append('Идет создание таблиц для отчетного месяца ' + year + ' ' + month)
        QApplication.instance().processEvents()
        create_tables(year + month)

    i_infinity = 0
    while i_infinity < 10:

        slpu = get_glpu()

        for lpu in slpu:
            glpu = lpu[0]
            name_mo = lpu[3]

            if exist(dir_XmlZip, year, month, glpu):
                time_start = timeit.default_timer()
                # Получаю файл ZIP из папки VipNet
                pathfile_zip = exist(dir_XmlZip, year, month, glpu)
                sleep(1)
                # Копирую архив во временную папку
                copy(pathfile_zip, tmp)
                # Получаю новый путь из временной папки
                tmp_zip = exist(tmp, year, month, glpu)
                # Извлекаю из архива файлы и удаляю архив = True
                extract(tmp_zip, tmp, True)
                get_file_xml(tmp_zip, year, month, glpu)
                tm_wr = str(timeit.default_timer() - time_start)
                tm_wr2 = timeit.default_timer() - time_start
                tt = msectohmc.display_time(tm_wr2)
                print(tmp_zip + ' ' + name_mo.strip() + ' время обработки: ' + tm_wr[0: 5])

                self.ui.textEdit.append(tmp_zip + '\n' +
                                        '  ==> ' + name_mo.strip() + '\n' +
                                        '  ==> дата/время: ' + strftime("%d.%m.%Y %H:%M:%S", localtime()) + '\n' +
                                        '  ==> время обработки: ' + tt + '\n')
                QApplication.instance().processEvents()