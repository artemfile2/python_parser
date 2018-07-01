from file_exist import *
from file_extract import *
from file_copy import *
import timeit
from time import strftime, localtime, sleep
from xml_todb import *
from connect import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
import msectohmc


def CreateTables(self, name_table):
    """
        Функция создания таблиц
    """
    try:
        db = con('db')
        dbcur = db.cursor()
        queryCreate = """CREATE TABLE ST05S50201807 (
                          ID_SCH VARCHAR2(25 BYTE),
                          VPOLIS NUMBER(*, 0),
                          SPOLIS VARCHAR2(10 BYTE),
                          NPOLIS VARCHAR2(20 BYTE),
                          SMO VARCHAR2(5 BYTE),
                          SMO_OGRN VARCHAR2(15 BYTE),
                          SMO_OK VARCHAR2(5 BYTE),
                          SMO_NAM VARCHAR2(50 BYTE),
                          NOVOR VARCHAR2(8 BYTE),
                          FAM VARCHAR2(40 BYTE),
                          IM VARCHAR2(40 BYTE),
                          OT VARCHAR2(40 BYTE),
                          W NUMBER(*, 0),
                          DR DATE,
                          FAM_P VARCHAR2(40 BYTE),
                          IM_P VARCHAR2(40 BYTE),
                          OT_P VARCHAR2(40 BYTE),
                          W_P NUMBER(*, 0),
                          DR_P DATE,
                          MR VARCHAR2(60 BYTE),
                          DOCTYPE NUMBER(*, 0),
                          DOCSER VARCHAR2(10 BYTE),
                          DOCNUM VARCHAR2(20 BYTE),
                          SNILS VARCHAR2(15 BYTE),
                          ADRES VARCHAR2(80 BYTE),
                          STAT NUMBER(*, 0),
                          POLIS VARCHAR2(30 BYTE) NOT NULL,
                          ID_PAC VARCHAR2(36 BYTE),
                          VNOV_D VARCHAR2(10 BYTE),
                          GLPU VARCHAR2(6 BYTE),
                          DOST VARCHAR2(10 BYTE),
                          DOST_P VARCHAR2(10 BYTE),
                          IDENT_SP VARCHAR2(10 BYTE),
                          INV NUMBER(*, 0)
                          )
                          TABLESPACE SYSTEM
                          STORAGE (INITIAL 64 K
                                 MAXEXTENTS UNLIMITED)
                          LOGGING                          
                          """
        dbcur.execute(queryCreate)
        queryIndex = """CREATE UNIQUE INDEX UK_ST05S50201807 ON ST05S50201807 (ID_PAC, GLPU)
                        TABLESPACE SYSTEM
                        STORAGE (INITIAL 64 K
                                 MAXEXTENTS UNLIMITED)
                        LOGGING"""
        dbcur.execute(queryIndex)
        db.commit()
        dbcur.close()

    except cx_Oracle.Error as err:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Query error: {}".format(err))
        msg.setWindowTitle("Ошибка в запросе")
        msg.setDetailedText("Query error: {}".format(err))
        msg.exec_()
        print("Query error: {}".format(err))


def CheckTable(name_table):
    """
        Функция проверки есть ли такие таблицы
    """
    try:
        db = con('db')
        dbcur = db.cursor()
        queryCheck = """SELECT TABLE_NAME FROM ALL_TABLES WHERE UPPER(TABLE_NAME) = UPPER({!r})""".format(name_table)
        dbcur.execute(queryCheck)
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


"""
Функция работы с архивом
"""
def extractZipXml(self, year, month, dir_XmlZip, tmp):

    if CheckTable('ST05S50' + year + month):
        self.ui.textEdit.append('Таблицы за отчетный период ' + year + ' ' + month +
                                ' найдены, данные с XML загружаются...')
        QApplication.instance().processEvents()
    else:
        self.ui.textEdit.append('Идет создание таблиц для отчетного месяца ' + year + ' ' + month)
        QApplication.instance().processEvents()
        CreateTables(self, 'ST05S50' + year + month)


    i_infinity = 0
    while i_infinity < 10:

        slpu = get_glpu()

        for lpu in slpu:
            glpu = lpu[0]
            name_mo = lpu[3] #get_slpuonglpu(glpu)

            if exist(dir_XmlZip, year, month, glpu):
                time_start = timeit.default_timer()
                #Получаю файл ZIP из папки VipNet
                pathfile_zip = exist(dir_XmlZip, year, month, glpu)
                sleep(1)
                #Копирую архив во временную папку
                copy(pathfile_zip, tmp)
                #Получаю новый путь из временной папки
                tmp_zip = exist(tmp, year, month, glpu)
                #Извлекаю из архива файлы и удаляю архив = True
                extract(tmp_zip, tmp, True)
                getFileXml(tmp_zip, year, month, glpu)
                tm_wr = str(timeit.default_timer() - time_start)
                tm_wr2 = timeit.default_timer() - time_start
                tt = msectohmc.display_time(tm_wr2)
                print(tmp_zip + ' ' + name_mo.strip() + ' время обработки: ' + tm_wr[0: 5])

                self.ui.textEdit.append(tmp_zip + '\n' +
                                        '  ==> ' + name_mo.strip() + '\n' +
                                        '  ==> дата/время: ' + strftime("%d.%m.%Y %H:%M:%S", localtime()) + '\n' +
                                        '  ==> время обработки: ' + tt + '\n')
                QApplication.instance().processEvents()