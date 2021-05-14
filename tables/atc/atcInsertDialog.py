import datetime

from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RefactorDialog(QDialog):
    customerAddedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.data = None

        self.setWindowTitle("Добавление ATC")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label_capt = QLabel("Название ATC:")
        self.label_address = QLabel("Адрес:")
        self.label_district = QLabel("Район:")
        self.label_date = QLabel("Дата открытия:")
        self.label_state = QLabel("Тип собственности:")
        self.label_license = QLabel("Лицензия:")

        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.caption = QLineEdit()
        self.address = QLineEdit()
        self.license = QLineEdit()
        self.date = QDateEdit()
        self.caption.setMaxLength(40)
        self.address.setMaxLength(40)

        self.state = QComboBox()
        self.state.addItems(["Государственная", "Частная"])

        district = []
        self.query = QSqlQuery()
        self.query.exec("""SELECT name_district FROM district""")
        while self.query.next():
            district.append(str(self.query.value(0)))
        self.district = QComboBox()
        self.district.addItems(district)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.gridlayout.addWidget(self.label_capt, 1, 0)
        self.gridlayout.addWidget(self.caption, 2, 0)
        self.gridlayout.addWidget(self.label_address, 3, 0)
        self.gridlayout.addWidget(self.address, 4, 0)
        self.gridlayout.addWidget(self.label_district, 5, 0)
        self.gridlayout.addWidget(self.district, 6, 0)
        self.gridlayout.addWidget(self.label_date, 1, 1)
        self.gridlayout.addWidget(self.date, 2, 1)
        self.gridlayout.addWidget(self.label_state, 3, 1)
        self.gridlayout.addWidget(self.state, 4, 1)
        self.gridlayout.addWidget(self.label_license, 5, 1)
        self.gridlayout.addWidget(self.license, 6, 1)
        self.gridlayout.addWidget(self.buttonsBox, 8, 0)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)
        self.buttonsBox.rejected.connect(self.reject)

    def data_validate(self):
        atc = self.caption.text()
        address = self.address.text()
        now = datetime.datetime.date(datetime.datetime.now())
        s = str(now)
        k = s.split("-")
        data = self.date.text()
        k2 = data.split(".")
        k2.reverse()
        if int(k2[0]) < 1876:
            messageBox = QMessageBox.warning(self, self.tr("Ошибка"),
                                             self.tr("Дата не может быть меньше 1876 года!"),
                                             QMessageBox.Ok)
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

    def insert(self):
        atc_name = self.caption.text()
        address = self.address.text()
        licens = self.license.text()
        name_district = self.district.currentText()
        data = self.date.text()
        state = self.state.currentText()
        if state == "Государственная":
            state_id = True
        else:
            state_id = False

        self.query.prepare("""SELECT id FROM district
                            WHERE name_district = ?;""")
        self.query.addBindValue(name_district)
        self.query.exec_()
        while self.query.next():
            district = self.query.value(0)
        if self.data_validate():
            if not atc_name or not address or not licens:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Необходимо заполнить все поля формы!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            else:
                self.query.prepare("INSERT INTO atc(caption, id_district, address, year, atc_state, license) "
                                   "VALUES (?, ?, ?, ?, ?, ?)")
                self.query.addBindValue(atc_name)
                self.query.addBindValue(district)
                self.query.addBindValue(address)
                self.query.addBindValue(data)
                self.query.addBindValue(state_id)
                self.query.addBindValue(licens)
                if not self.query.exec_():
                    messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("АТС с таким названием уже существует!"),
                                                      QMessageBox.Ok | QMessageBox.Cancel)
                else:
                    messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                         self.tr("Новая запись добавлена!"),
                                                         QMessageBox.Ok)
                    self.close()
