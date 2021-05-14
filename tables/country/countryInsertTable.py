from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RefactorDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.data = None
        self.query = QSqlQuery()
        self.setWindowTitle("Добавление страны")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label = QLabel("Название страны:")
        self.label_p = QLabel("Цена 1 мин")
        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")
        self.name_country_add = QLineEdit()
        self.price = QDoubleSpinBox()

        rx = QRegExp("[а-яА-Яa-zA-Z]+")
        validator = QRegExpValidator(rx, self)
        self.name_country_add.setValidator(validator)
        self.name_country_add.setMaxLength(20)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.gridlayout.addWidget(self.buttonsBox, 5, 0)
        self.gridlayout.addWidget(self.name_country_add, 1, 0)
        self.gridlayout.addWidget(self.label, 0, 0)
        self.gridlayout.addWidget(self.label_p, 3, 0)
        self.gridlayout.addWidget(self.price, 4, 0)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)
        self.buttonsBox.rejected.connect(self.reject)

    def insert(self):
        name = self.name_country_add.text()
        spin = self.price.value()
        if not name or not spin or len(name) == 0:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Необходимо заполнить все поля формы!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        elif len(name) < 3:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Название страны не "
                                                                                "может быть меньше 3 символов!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        else:
            self.query.prepare(
                "INSERT INTO country(name_country, price) "
                "VALUES (?, ?)")
            self.query.addBindValue(name)
            self.query.addBindValue(spin)

            if not self.query.exec_():
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Страна уже существует!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            else:
                messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                     self.tr("Новая запись добавлена!"),
                                                     QMessageBox.Ok)
                self.close()