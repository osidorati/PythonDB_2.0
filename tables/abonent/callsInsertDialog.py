from datetime import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RefactorDialog(QDialog):
    customerAddedSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()

        self.setWindowTitle("Добавление звонка")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label1 = QLabel("Абонент:")
        self.label2 = QLabel("Город:")
        self.label3 = QLabel("Телефон звонка:")
        self.label4 = QLabel("Дата:")
        self.label5 = QLabel("Продолжительность:")

        self.label6 = QLabel("Тариф:")

        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.number = QLineEdit('+38071')
        self.number.setMaxLength(13)
        self.duration = QLineEdit()
        self.date = QDateEdit()
        self.abonent = QLineEdit()
        self.city = QComboBox()
        self.tariff = QComboBox()

        self.duration.setValidator(QIntValidator(0, 1000, self))

        city = []
        self.query.exec("""SELECT name_city FROM city""")
        while self.query.next():
            city.append(self.query.value(0))
        self.city.addItems(city)

        tariff = []
        self.query.exec("""SELECT type_tariff FROM tariff""")
        while self.query.next():
            tariff.append(self.query.value(0))
        self.tariff.addItems(tariff)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.gridlayout.addWidget(self.label1, 1, 0)
        self.gridlayout.addWidget(self.label2, 2, 0)
        self.gridlayout.addWidget(self.label3, 3, 0)
        self.gridlayout.addWidget(self.label4, 4, 0)
        self.gridlayout.addWidget(self.label5, 5, 0)
        self.gridlayout.addWidget(self.label6, 6, 0)
        #self.gridlayout.addWidget(, 1, 0)
        self.gridlayout.addWidget(self.abonent, 1, 1)
        self.gridlayout.addWidget(self.city, 2, 1)
        self.gridlayout.addWidget(self.number, 3, 1)
        self.gridlayout.addWidget(self.date, 4, 1)
        self.gridlayout.addWidget(self.duration, 5, 1)
        self.gridlayout.addWidget(self.tariff, 6, 1)
        self.gridlayout.addWidget(self.buttonsBox, 8, 0)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)
        self.buttonsBox.rejected.connect(self.reject)

    def setIndex(self, index):
        self.index = index
        abonent = ""
        self.query.prepare("""SELECT surname, name, middlename, phone_number FROM abonents where id = ?""")
        self.query.addBindValue(self.index)
        self.query.exec_()
        while self.query.next():
            abonent = self.query.value(0) + " " + self.query.value(1) + " " + self.query.value(2) + " (" + self.query.value(3) + ")"
        self.abonent.setText(abonent)
        self.abonent.setReadOnly(True)

    def insert(self):
        abonent = self.abonent.text()
        abonent_data = abonent.split("(")
        abonent_data[1] = abonent_data[1].replace(")", "")
        abonent_num = abonent_data[1]

        city = self.city.currentText()
        number = self.number.text()
        date = self.date.text()
        try:
            duration = int(self.duration.text())
        except:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Укажите продолжительность звонка!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        tariff = self.tariff.currentText()

        self.query.prepare("""SELECT id FROM abonents
                            WHERE phone_number = ?;""")
        self.query.addBindValue(abonent_num)
        self.query.exec_()
        while self.query.next():
            abonent_id = self.query.value(0)

        self.query.prepare("""SELECT id FROM city
                                    WHERE name_city = ?;""")
        self.query.addBindValue(city)
        self.query.exec_()
        while self.query.next():
            city_id = self.query.value(0)

        self.query.prepare("""SELECT id FROM tariff
                                            WHERE type_tariff = ?;""")
        self.query.addBindValue(tariff)
        self.query.exec_()
        while self.query.next():
            tariff_id = self.query.value(0)
        if self.data_validate():
            if duration <= 0 or not duration or len(number) != 13:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Необходимо заполнить все поля формы!"),
                                                 QMessageBox.Ok | QMessageBox.Cancel)
            else:
                self.query.prepare(
                    "INSERT INTO calls(id_abonent, id_city, telephone_in, date, duration, id_tariff) "
                    "VALUES (?, ?, ?, ?, ?, ?)")
                self.query.addBindValue(abonent_id)
                self.query.addBindValue(city_id)
                self.query.addBindValue(number)
                self.query.addBindValue(date)
                self.query.addBindValue(duration)
                self.query.addBindValue(tariff_id)

                if not self.query.exec_():
                    messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("Звонок уже существует!"),
                                                      QMessageBox.Ok | QMessageBox.Cancel)
                else:
                    messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                      self.tr("Новая запись добавлена!"),
                                                      QMessageBox.Ok)
                    self.close()

    def data_validate(self):
        now = datetime.date(datetime.now())
        s = str(now)
        k = s.split("-")
        data = self.date.text()
        k2 = data.split(".")
        k2.reverse()
        if k2[0] > k[0] or (k2[0] == k[0] and k2[1] > k[1] or (k2[0] == k[0] and k2[1] == k[1] and k2[2] > k[2])):
            messageBox = QMessageBox.warning(self, self.tr("Ошибка"),
                                             self.tr("Дата не может быть больше текущей!"),
                                             QMessageBox.Ok)
            return False
        else:
            return True




