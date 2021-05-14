from datetime import datetime

from PyQt5.QtGui import QFont
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
        self.box = QComboBox()
        district = []
        self.query = QSqlQuery()
        self.query.exec("""SELECT name_district FROM district""")
        while self.query.next():
            district.append(str(self.query.value(0)))
        self.district = QComboBox()
        self.box.addItems(district)

        self.box2 = QComboBox()
        state = ['False', 'True']
        self.box2.addItems(state)

        self.atc = QLineEdit()
        self.license = QLineEdit()
        self.address = QLineEdit()
        self.data = QDateEdit()

        self.label1 = QLabel("Название АТС:")
        self.label2 = QLabel("Район:")
        self.label3 = QLabel("Адрес:")
        self.label4 = QLabel("Дата основания:")
        self.label5 = QLabel("Статус АТС:")
        self.label6 = QLabel("Лицензия:")

        self.save_btn = QPushButton("Сохранить изменения")
        self.cancel_btn = QPushButton("Cancel")

        self.gridlayout.addWidget(self.label1, 1, 0)
        self.gridlayout.addWidget(self.label2, 2, 0)
        self.gridlayout.addWidget(self.label3, 3, 0)
        self.gridlayout.addWidget(self.label4, 4, 0)
        self.gridlayout.addWidget(self.label5, 5, 0)
        self.gridlayout.addWidget(self.label6, 6, 0)

        self.gridlayout.addWidget(self.atc, 1, 1)
        self.gridlayout.addWidget(self.box, 2, 1)
        self.gridlayout.addWidget(self.address, 3, 1)
        self.gridlayout.addWidget(self.data, 4, 1)
        self.gridlayout.addWidget(self.box2, 5, 1)
        self.gridlayout.addWidget(self.license, 6, 1)

        self.gridlayout.addWidget(self.save_btn, 12, 0)
        self.gridlayout.addWidget(self.cancel_btn, 12, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        #self.cancel_btn.clicked.connect()
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.cancel)

    def save(self):
        atc = self.atc.text()
        address = self.address.text()
        licens = self.license.text()
        name_district = self.box.currentText()
        data = self.data.text()
        state = self.box2.currentText()
        self.query.prepare("""SELECT id FROM district
                                    WHERE name_district = ?;""")
        self.query.addBindValue(name_district)
        self.query.exec_()
        while self.query.next():
            district = self.query.value(0)
        if self.data_validate():
            if not atc or not address or not licens:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("Необходимо заполнить все поля формы!"),
                                                      QMessageBox.Ok | QMessageBox.Cancel)
            else:
                self.query.prepare("UPDATE atc SET caption = ?, id_district = ?, address = ?, "
                                       "year = ?, atc_state = ?, license = ? "
                                        " WHERE id_atc = ? RETURNING *;")
                self.query.addBindValue(atc)
                self.query.addBindValue(district)
                self.query.addBindValue(address)
                self.query.addBindValue(data)
                self.query.addBindValue(state)
                self.query.addBindValue(licens)
                self.query.addBindValue(self.index)
                if not self.query.exec_():
                    messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                          self.tr("АТС с таким данными уже существует!"),
                                                          QMessageBox.Ok | QMessageBox.Cancel)
                else:
                    messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                             self.tr("Запись изменена!"),
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
        query.prepare("""select atc.caption, district.name_district, atc.address, 
                                    atc.year, atc.atc_state, atc.license 
                                    from atc join district on atc.id_district = district.id where atc.id_atc = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(6):
                data.append(query.value(i))
        self.atc.setText(data[0])
        self.box.setCurrentText(data[1])
        self.address.setText(data[2])
        self.data.setDate(data[3])
        self.license.setText(str(data[5]))
        self.box2.setCurrentText(str(data[4]))

    def data_validate(self):
        atc = self.caption.text()
        address = self.address.text()
        now = datetime.datetime.date(datetime.datetime.now())
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
        elif atc.isdigit() == True or address.isdigit() == True:
            messageBox = QMessageBox.warning(self, self.tr("Ошибка"),
                                             self.tr("Название АТС или адрес не могут состоять только из цифр!"),
                                             QMessageBox.Ok)
        elif len(atc) < 5 or len(address) < 5:
            messageBox = QMessageBox.warning(self, self.tr("Ошибка"),
                                             self.tr("Название АТС или адрес не могут быть меньше 5 символов!"),
                                             QMessageBox.Ok)
        else:
            return True

    def data_validate(self):
        surname = self.surname.text()
        name = self.name.text()
        middlename = self.middlename.text()
        address = self.address.text()
        if len(surname) < 3 or len(address) < 3 or len(name) < 3 or len(middlename) < 3:
            messageBox = QMessageBox.warning(self, self.tr("Ошибка"),
                                             self.tr("ФИО или адрес не могут быть меньше 3 символов!"),
                                             QMessageBox.Ok)
            return False
        elif address.isdigit():
            messageBox = QMessageBox.warning(self, self.tr("Ошибка"),
                                             self.tr("Адрес не может состоять только из цифр!"),
                                             QMessageBox.Ok)
        else:
            return True




