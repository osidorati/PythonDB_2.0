from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RefactorDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.data = None

        self.setWindowTitle("Добавление района")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label_distr = QLabel("Название города:")
        self.label_country = QLabel("Выберите страну:")
        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")
        self.name_district_add = QLineEdit()

        country = []
        self.query = QSqlQuery()
        self.query.exec("""SELECT name_country FROM country""")
        while self.query.next():
            country.append(str(self.query.value(0)))
        self.country = QComboBox()
        self.country.addItems(country)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        rx = QRegExp("[а-яА-Яa-zA-Z]+")
        validator = QRegExpValidator(rx, self)
        self.name_district_add.setValidator(validator)
        self.name_district_add.setMaxLength(20)

        self.gridlayout.addWidget(self.buttonsBox, 5, 0)
        self.gridlayout.addWidget(self.country, 1, 0)
        self.gridlayout.addWidget(self.label_country, 0, 0)
        self.gridlayout.addWidget(self.label_distr, 2, 0)
        self.gridlayout.addWidget(self.name_district_add, 3, 0)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)
        self.buttonsBox.rejected.connect(self.reject)

    def insert(self):
        country = self.country.currentText()
        city = self.name_district_add.text()

        self.query.prepare("""SELECT id FROM country
                                    WHERE name_country = ?;""")
        self.query.addBindValue(country)
        self.query.exec_()
        while self.query.next():
            country_id = self.query.value(0)

        if not city:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Необходимо заполнить все поля формы!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
        elif len(city) < 2:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                              self.tr("Название города не может быть меньше 2 символов!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        else:
            self.query.prepare("INSERT INTO city(id_country, name_city) "
                                   "VALUES (?, ?)")
            self.query.addBindValue(country_id)
            self.query.addBindValue(city)
            if not self.query.exec_():
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("Горож с таким названием уже существует!"),
                                                      QMessageBox.Ok | QMessageBox.Cancel)
            else:
                messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                         self.tr("Новая запись добавлена!"),
                                                         QMessageBox.Ok)
                self.close()