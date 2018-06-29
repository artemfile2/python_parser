from main_form import *
import sys
from work_xml import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon



class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setPlaceholderText("Пример: 2018")
        self.ui.lineEdit_2.setPlaceholderText("Пример: 07")

        self.setWindowTitle('ParserXMLORCL')
        self.setWindowIcon(QIcon('00011.ico'))

        # Этой строчкой мы вешаем на кнопку нашу новую функцию
        # под названием Check
        self.ui.pushButton.clicked.connect(self.Check)
        self.show()

    # Собственно описываем функцию Check
    # которая вызывается при нажатии кнопки
    def Check(self):
        # Каталог из которого будем брать файлы
        dir_XmlZip = 'C:\\temp\\2\\IN\\'
        # Временный каталог
        tmp = 'C:\\txt\\'

        year = self.ui.lineEdit.text()
        month = self.ui.lineEdit_2.text()

        extractZipXml(self, year, month, dir_XmlZip, tmp)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())