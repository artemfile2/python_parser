# -*- coding: utf-8 -*-

from main_form import *
import sys
from work_xml import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread

from connect import *


class MyWin(QtWidgets.QMainWindow, QThread):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        QThread.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setPlaceholderText("Пример: 2018")
        self.ui.lineEdit_2.setPlaceholderText("Пример: 07")

        self.setWindowTitle('ParserXMLORCL')
        self.setWindowIcon(QIcon('00011.ico'))

        # Этой строчкой мы вешаем на кнопку нашу новую функцию
        # под названием Check
        self.ui.pushButton.clicked.connect(self.check)
        self.show()

        db = con('db')
        if type(db) == list:
            self.ui.textEdit.append(db[1])


    # Собственно описываем функцию Check
    # которая вызывается при нажатии кнопки
    def check(self):
        # Каталог из которого будем брать файлы
        dir_XmlZip = 'C:\\temp\\2\\IN\\'
        # Временный каталог
        tmp = 'C:\\txt\\zip\\'

        year = self.ui.lineEdit.text()
        month = self.ui.lineEdit_2.text()

        if year == '' or month == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Введите все данные. Не ввели ГОД или МЕСЯЦ")
            msg.setWindowTitle("Введите все данные")
            msg.exec_()
        else:
            if int(year) not in range(2018, 2019):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Год не является корректным!")
                msg.setWindowTitle("Исправить год!")
                msg.exec_()
            else:
                self.ui.pushButton.setText('Остановить')
                self.ui.pushButton.setEnabled(False)
                # self.thread1 = QThread()  # создаем поток
                # self.thread1.progress.connect(self.setFirstPbar)
                extractZipXml(self, year, month, dir_XmlZip, tmp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())