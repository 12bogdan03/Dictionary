import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.word_input = QtWidgets.QLineEdit('Введіть слово', self)
        self.search_btn = QtWidgets.QPushButton('Пошук', self)
        self.search_btn.setObjectName("search_btn")
        self.lemmatize_checkbox = QtWidgets.QCheckBox('Лематизувати', self)
        self.letters_list = QtWidgets.QListWidget(self)
        self.label_alphabetical_index = QtWidgets.QLabel('<html><head/><body><p>'
                                                         '<span style=\" font-size:14pt;'
                                                         ' font-weight:600;\">'
                                                         'Алфавітний покажчик'
                                                         '</span></p></body></html>',
                                                         self)
        self.setupUi()

    def setupUi(self):
        self.word_input.setGeometry(QtCore.QRect(30, 30, 341, 25))
        self.word_input.setObjectName("word_input")
        self.search_btn.setGeometry(QtCore.QRect(570, 30, 141, 25))

        self.lemmatize_checkbox.setGeometry(QtCore.QRect(410, 30, 151, 23))
        self.lemmatize_checkbox.setObjectName("lemmatize_checkbox")

        self.letters_list.setGeometry(QtCore.QRect(30, 140, 681, 50))
        self.letters_list.setObjectName("letters_list")
        self.letters_list.setFlow(QtWidgets.QListWidget.LeftToRight)
        self.fill_alphabet_box()

        self.label_alphabetical_index.setGeometry(QtCore.QRect(30, 90, 291, 31))
        self.label_alphabetical_index.setObjectName("label_alphabetical_index")

        self.setWindowTitle('Словник колокацій')
        self.center()
        self.show()

    def fill_alphabet_box(self):
        alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
        for i in alphabet:
            self.letters_list.addItem(
                QtWidgets.QListWidgetItem(i)
            )

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
