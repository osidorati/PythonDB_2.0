from datetime import datetime

from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ChangeDialog(QDialog):
    customerAddedSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.setWindowTitle("Просмотр сведений об абоненте")
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.model = QSqlQueryModel(self)

        self.label1 = QLabel("Абонент:")
        self.label2 = QLabel("Город:")
        self.label3 = QLabel("Телефон звонка:")
        self.label4 = QLabel("Дата:")
        self.label5 = QLabel("Продолжительность:")
        self.label6 = QLabel("Тариф:")
        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.number = QLineEdit()
        self.duration = QLineEdit()
        self.date = QDateEdit()
        self.abonent = QComboBox()
        self.city = QComboBox()
        self.tariff = QComboBox()
        self.save_btn = QPushButton("Сохранить изменения")
        self.cancel_btn = QPushButton("Cancel")

        self.duration.setValidator(QIntValidator(0, 1000, self))

        abonent = []
        self.query.exec("""SELECT surname, name, middlename, phone_number FROM abonents""")
        while self.query.next():
            name = self.query.value(0) + " " + self.query.value(1) + " " + self.query.value(
                2) + "\n" + self.query.value(3)
            abonent.append(name)
        self.abonent.addItems(abonent)

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

        self.label1 = QLabel("Абонент:")
        self.label2 = QLabel("Город:")
        self.label3 = QLabel("Телефон звонка:")
        self.label4 = QLabel("Дата:")
        self.label5 = QLabel("Продолжительность:")
        self.label6 = QLabel("Тариф:")
        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.gridlayout.addWidget(self.label1, 1, 0)
        self.gridlayout.addWidget(self.label2, 2, 0)
        self.gridlayout.addWidget(self.label3, 3, 0)
        self.gridlayout.addWidget(self.label4, 4, 0)
        self.gridlayout.addWidget(self.label5, 5, 0)
        self.gridlayout.addWidget(self.label6, 6, 0)

        self.gridlayout.addWidget(self.abonent, 1, 1)
        self.gridlayout.addWidget(self.city, 2, 1)
        self.gridlayout.addWidget(self.number, 3, 1)
        self.gridlayout.addWidget(self.date, 4, 1)
        self.gridlayout.addWidget(self.duration, 5, 1)
        self.gridlayout.addWidget(self.tariff, 6, 1)
        self.gridlayout.addWidget(self.save_btn, 12, 0)
        self.gridlayout.addWidget(self.cancel_btn, 12, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.cancel)

    def save(self):
        abonent = self.abonent.currentText()
        abonent_data = abonent.split("\n")
        abonent_num = abonent_data[1]

        city = self.city.currentText()
        number = self.number.text()
        date = self.date.text()
        try:
            duration = int(self.duration.text())
        except:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("!"),
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
                    "UPDATE calls SET id_abonent = ?, id_city = ?, telephone_in = ?, date = ?, duration = ?, id_tariff = ? "
                    "WHERE ID = ?")
                self.query.addBindValue(abonent_id)
                self.query.addBindValue(city_id)
                self.query.addBindValue(number)
                self.query.addBindValue(date)
                self.query.addBindValue(duration)
                self.query.addBindValue(tariff_id)
                self.query.addBindValue(self.index)
                if not self.query.exec_():
                    messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("Звонок уже существует!"),
                                                      QMessageBox.Ok | QMessageBox.Cancel)
                else:
                    messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                         self.tr("Новая запись добавлена!"),
                                                         QMessageBox.Ok)
                    self.close()

    def cancel(self):
        self.close()

    def setIndex(self, index):
        self.index = index
        self.setData()

    def setData(self):
        query = QSqlQuery()
        data = []
        query.prepare("""select abonents.surname, abonents.name, abonents.middlename, abonents.phone_number, 
        city.name_city, calls.telephone_in, calls.date, calls.duration, tariff.type_tariff 
        from calls join abonents on calls.id_abonent = abonents.id 
        join city on calls.id_city = city.id 
        join tariff on calls.id_tariff = tariff.id
        where calls.id = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(9):
                data.append(query.value(i))
        self.abonent.setCurrentText(data[0] + " " + data[1] + " " + data[2] + "\n" + data[3])
        self.city.setCurrentText(data[4])
        self.number.setText(data[5])
        self.tariff.setCurrentText(data[8])
        self.duration.setText(str(data[7]))
        self.date.setDate(data[6])


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





