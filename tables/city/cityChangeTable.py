from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ChangeDialog(QDialog):

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
        self.label_country = QLabel("Cтранa:")
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
        self.save_btn = QPushButton("Сохранить изменения")
        self.cancel_btn = QPushButton("Cancel")

        rx = QRegExp("[а-яА-Яa-zA-Z]+")
        validator = QRegExpValidator(rx, self)
        self.name_district_add.setValidator(validator)
        self.name_district_add.setMaxLength(20)

        self.gridlayout.addWidget(self.country, 1, 0)
        self.gridlayout.addWidget(self.label_country, 0, 0)
        self.gridlayout.addWidget(self.label_distr, 2, 0)
        self.gridlayout.addWidget(self.name_district_add, 3, 0)
        self.gridlayout.addWidget(self.save_btn, 12, 0)
        self.gridlayout.addWidget(self.cancel_btn, 12, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.cancel)

    def cancel(self):
        self.close()

    def setIndex(self, index):
        self.index = index
        self.setData()

    def setData(self):
        query = QSqlQuery()
        data = []
        query.prepare("select country.name_country, city.name_city "
                    "from city join country on city.id_country = country.id where city.id = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(2):
                data.append(query.value(i))
        self.name_district_add.setText(data[1])
        self.country.setCurrentText(data[0])

    def save(self):
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
            self.query.prepare("UPDATE city SET id_country = ?, name_city = ? "
                                   "WHERE id = ?")
            self.query.addBindValue(country_id)
            self.query.addBindValue(city)
            self.query.addBindValue(self.index)
            if not self.query.exec_():
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("Город с таким названием уже существует!"),
                                                      QMessageBox.Ok | QMessageBox.Cancel)
            else:
                messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                         self.tr("Запись изменена!"),
                                                         QMessageBox.Ok)
                self.close()