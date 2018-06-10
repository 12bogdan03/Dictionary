import sys
import sqlite3

from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.style = QtWidgets.QComboBox(self)
        self.word_input = QtWidgets.QLineEdit('Введіть слово', self)
        self.search_btn = QtWidgets.QPushButton('Пошук', self)
        self.lemmatize_checkbox = QtWidgets.QCheckBox('Пошук за лемами', self)
        self.letters_list = QtWidgets.QListWidget(self)
        self.label_alphabetical_index = QtWidgets.QLabel('<html><head/><body><p>'
                                                         '<span style=\" font-size:14pt;'
                                                         ' font-weight:600;\">'
                                                         'Алфавітний покажчик'
                                                         '</span></p></body></html>',
                                                         self)
        self.search_results = QtWidgets.QListWidget(self)

        self.db_conn = sqlite3.connect('context.db')
        self.db_cursor = self.db_conn.cursor()

        self.setupUi()

    def setupUi(self):
        self.style.addItems(['Всі стилі', 'Художня проза',
                             'Науковий стиль', 'Публіцистика'])
        self.style.setGeometry(QtCore.QRect(420, 90, 290, 31))

        self.word_input.setGeometry(QtCore.QRect(30, 30, 341, 25))
        self.word_input.setObjectName("word_input")
        self.search_btn.setGeometry(QtCore.QRect(570, 30, 141, 25))
        self.search_btn.setObjectName("search_btn")
        self.search_btn.clicked.connect(self.search_word)

        self.lemmatize_checkbox.setGeometry(QtCore.QRect(410, 30, 151, 23))
        self.lemmatize_checkbox.setObjectName("lemmatize_checkbox")

        self.letters_list.setGeometry(QtCore.QRect(30, 140, 681, 50))
        self.letters_list.setObjectName("letters_list")
        self.letters_list.setSpacing(2)
        self.letters_list.setFlow(QtWidgets.QListWidget.LeftToRight)
        self.letters_list.itemClicked.connect(self.search_by_initial_letter)
        self.fill_alphabet_box()

        self.label_alphabetical_index.setGeometry(QtCore.QRect(30, 90, 291, 31))
        self.label_alphabetical_index.setObjectName("label_alphabetical_index")

        self.search_results.setGeometry(QtCore.QRect(30, 200, 681, 360))
        self.search_results.addItem("Тут будуть відображені результати пошуку.")

        self.setWindowTitle('Словник колокацій')
        self.center()
        self.show()

    def fill_alphabet_box(self):
        alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯ'
        for i in alphabet:
            self.letters_list.addItem(
                QtWidgets.QListWidgetItem(i)
            )

    def center(self):
        self.setFixedSize(750, 600)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def search_word(self):
        table_names = {
            'Художня проза': 'context_hp',
            'Науковий стиль': 'context_nauk',
            'Публіцистика': 'context_pb'
        }

        search_for = self.word_input.text()
        if self.lemmatize_checkbox.isChecked():
            unit1, unit2 = 'lem1', 'lem2'
        else:
            unit1, unit2 = 'word1', 'word2'

        if self.style.currentText() == 'Всі стилі':
            self.db_cursor.execute("""
                SELECT word1, word2 FROM context_hp
                WHERE {0}="{2}" OR {1}="{2}"
                UNION
                SELECT word1, word2  FROM context_nauk
                WHERE {0}="{2}" OR {1}="{2}"
                UNION
                SELECT word1, word2  FROM context_pb
                WHERE {0}="{2}" OR {1}="{2}"
            """.format(unit1, unit2, search_for))
        else:
            self.db_cursor.execute("""
                SELECT word1, word2 FROM {0} 
                WHERE {1}="{3}" OR {2}="{3}"
            """.format(table_names[self.style.currentText()],
                       unit1, unit2, search_for))
        contexts = set([' '.join(i) for i in self.db_cursor.fetchall()])
        self.search_results.clear()
        if contexts:
            self.search_results.addItems(contexts)
        else:
            self.search_results.addItem('Нічого не знайдено :(')

    def search_by_initial_letter(self):
        table_names = {
            'Художня проза': 'context_hp',
            'Науковий стиль': 'context_nauk',
            'Публіцистика': 'context_pb'
        }

        letter = self.letters_list.currentItem().text()
        if self.style.currentText() == 'Всі стилі':
            self.db_cursor.execute("""
                        SELECT word1, word2 FROM context_hp
                        WHERE word1 LIKE "{0}%" OR word2 LIKE "{0}%" 
                              OR word1 LIKE "{1}%" OR word2 LIKE "{1}%"
                        UNION
                        SELECT word1, word2 FROM context_nauk
                        WHERE word1 LIKE "{0}%" OR word2 LIKE "{0}%" 
                              OR word1 LIKE "{1}%" OR word2 LIKE "{1}%"
                        UNION
                        SELECT word1, word2 FROM context_pb
                        WHERE word1 LIKE "{0}%" OR word2 LIKE "{0}%" 
                              OR word1 LIKE "{1}%" OR word2 LIKE "{1}%"
                    """.format(letter, letter.lower()))
        else:
            self.db_cursor.execute("""
                        SELECT word1, word2 FROM {0} 
                        WHERE word1 LIKE "{0}%" OR word2 LIKE "{0}%" 
                              OR word1 LIKE "{2}%" OR word2 LIKE "{2}%"
                    """.format(table_names[self.style.currentText()],
                               letter, letter.lower()))
        contexts = set([' '.join(i) for i in self.db_cursor.fetchall()])
        self.search_results.clear()
        if contexts:
            self.search_results.addItems(contexts)
        else:
            self.search_results.addItem('Нічого не знайдено :(')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
