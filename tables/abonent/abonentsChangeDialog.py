from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ChangeDialog(QDialog):
    customerAddedSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        caption = []
        benefit = []
        position = []

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

        self.label1 = QLabel("Фамилия:")
        self.label2 = QLabel("Имя:")
        self.label3 = QLabel("Отчество:")
        self.label4 = QLabel("АТС:")
        self.label5 = QLabel("Номер телефона:")
        self.label6 = QLabel("Адрес:")
        self.label7 = QLabel("Социальное положение:")
        self.label8 = QLabel("Льгота:")
        self.label9 = QLabel("Документ на льготу:")

        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.middlename = QLineEdit()
        self.address = QLineEdit()
        self.number = QLineEdit()
        self.atc = QComboBox()
        self.position = QComboBox()
        self.benefit = QComboBox()
        self.file = QLabel()

        self.number.setMaxLength(13)
        rx = QRegExp("[а-яА-Яa-zA-Z]+")
        validator = QRegExpValidator(rx, self)
        self.surname.setValidator(validator)
        self.name.setValidator(validator)
        self.middlename.setValidator(validator)
        self.surname.setMaxLength(20)
        self.name.setMaxLength(20)
        self.middlename.setMaxLength(20)
        self.address.setMaxLength(40)

        self.query.exec("""SELECT caption FROM atc""")
        while self.query.next():
            caption.append(self.query.value(0))

        self.query.exec("""SELECT type_positon FROM position """)
        while self.query.next():
            position.append(self.query.value(0))

        benefit.append(None)
        self.query.exec("""SELECT type FROM benefit""")
        while self.query.next():
            benefit.append(self.query.value(0))

        self.atc.addItems(caption)
        self.position.addItems(position)
        self.benefit.addItems(benefit)

        self.save_btn = QPushButton("Сохранить изменения")
        self.cancel_btn = QPushButton("Cancel")

        self.gridlayout.addWidget(self.label4, 1, 0)
        self.gridlayout.addWidget(self.label1, 2, 0)
        self.gridlayout.addWidget(self.label2, 3, 0)
        self.gridlayout.addWidget(self.label3, 4, 0)
        self.gridlayout.addWidget(self.label5, 5, 0)
        self.gridlayout.addWidget(self.label6, 6, 0)
        self.gridlayout.addWidget(self.label7, 7, 0)
        self.gridlayout.addWidget(self.label8, 8, 0)
        self.gridlayout.addWidget(self.label9, 9, 0)

        self.gridlayout.addWidget(self.atc, 1, 1, 1, 3)
        self.gridlayout.addWidget(self.surname, 2, 1, 1, 3)
        self.gridlayout.addWidget(self.name, 3, 1, 1, 3)
        self.gridlayout.addWidget(self.middlename, 4, 1, 1, 3)
        self.gridlayout.addWidget(self.number, 5, 1, 1, 3)
        self.gridlayout.addWidget(self.address, 6, 1, 1, 3)
        self.gridlayout.addWidget(self.position, 7, 1, 1, 3)
        self.gridlayout.addWidget(self.benefit, 8, 1, 1, 3)
        self.gridlayout.addWidget(self.file, 9, 2)

        self.gridlayout.addWidget(self.save_btn, 12, 0)
        self.gridlayout.addWidget(self.cancel_btn, 12, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.cancel)

    def save(self):
        atc = self.atc.currentText()
        surname = self.surname.text()
        name = self.name.text()
        middlename = self.middlename.text()
        address = self.address.text()
        number = self.number.text()
        position = self.position.currentText()
        benefit = self.benefit.currentText()
        document = self.file.text()

        self.query.prepare("""SELECT id_atc FROM atc
                                   WHERE caption = ?;""")
        self.query.addBindValue(atc)
        self.query.exec_()
        while self.query.next():
            atc_id = self.query.value(0)

        self.query.prepare("""SELECT id FROM position
                                           WHERE type_positon = ?;""")
        self.query.addBindValue(position)
        self.query.exec_()
        while self.query.next():
            position_id = self.query.value(0)

        if len(benefit) == 0:
            benefit_id = None
        else:
            self.query.prepare("""SELECT id FROM benefit
                                               WHERE type = ?;""")
            self.query.addBindValue(benefit)
            self.query.exec_()
            while self.query.next():
                benefit_id = self.query.value(0)
        if self.data_validate():
            if not surname or not name or not middlename or not address:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Необходимо заполнить все поля формы!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            elif benefit_id is None and len(document) > 2:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Выберите тип льготы или удалите фото льготы!"),
                                                  QMessageBox.Ok)
            elif benefit_id is not None and len(document) < 2:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Добавьте фото льготы или уберите льготу!"),
                                                  QMessageBox.Ok)
            elif len(number) != 13:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Номер телефона не может быть больше или меньше 13 символов!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            else:
                self.query.prepare(
                    "UPDATE abonents SET id_atc = ?, surname = ?, name = ?, middlename = ?, phone_number = ?, address = ?, "
                    "id_position = ?, id_benefit = ?, document = ? "
                    " WHERE id = ? RETURNING *;")
                self.query.addBindValue(atc_id)
                self.query.addBindValue(surname)
                self.query.addBindValue(name)
                self.query.addBindValue(middlename)
                self.query.addBindValue(number)
                self.query.addBindValue(address)
                self.query.addBindValue(position_id)
                self.query.addBindValue(benefit_id)
                self.query.addBindValue(document)
                self.query.addBindValue(self.index)
                if not self.query.exec_():
                    messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("Абонент уже существует!"),
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
        query.prepare("""select atc.caption, abonents.surname, abonents.name, abonents.middlename, 
                        abonents.phone_number, abonents.address, 
                        position.type_positon, benefit.type, abonents.document 
                        from abonents 
                        join atc on abonents.id_atc = atc.id_atc
                        join position on abonents.id_position = position.id
                        left join benefit on abonents.id_benefit = benefit.id
                        where abonents.id = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(9):
                data.append(query.value(i))
        self.atc.setCurrentText(data[0])
        self.surname.setText(data[1])
        self.name.setText(data[2])
        self.middlename.setText(data[3])
        self.number.setText(data[4])
        self.address.setText(data[5])
        self.position.setCurrentText(data[6])
        self.benefit.setCurrentText(data[7])
        self.file.setText(data[8])


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




