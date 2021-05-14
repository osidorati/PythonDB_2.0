from datetime import datetime

from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RefactorDialog(QDialog):
    customerAddedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        caption = []
        position = []
        benefit = []
        self.fname = ""

        self.setWindowTitle("Добавление абонента")
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label1 = QLabel("Фамилия:")
        self.label2 = QLabel("Имя:")
        self.label3 = QLabel("Отчество:")
        self.label4 = QLabel("АТС:")
        self.label5 = QLabel("Номер телефона:")
        self.label6 = QLabel("Адрес:")
        self.label7 = QLabel("Социальное положение:")
        self.label8 = QLabel("Льгота:")
        self.label9 = QLabel("Документ на льготу:")

        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.middlename = QLineEdit()
        self.address = QLineEdit()
        self.number = QLineEdit('+38071')
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

        self.atc = QComboBox()
        self.position = QComboBox()
        self.benefit = QComboBox()
        self.file = QPushButton("Загрузить фото...")

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

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

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
        self.gridlayout.addWidget(self.buttonsBox, 11, 1, 1, 2)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)
        self.buttonsBox.rejected.connect(self.reject)
        self.file.clicked.connect(self.load_photo)

    def load_photo(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/img', "Image Files (*.png *.jpg)")[0]
        l = self.fname.split('/')
        self.label_file = QLabel(l[len(l) - 1])
        self.delete = QPushButton("Удалить..")
        self.gridlayout.addWidget(self.label_file, 9, 1)
        self.gridlayout.addWidget(self.delete, 9, 3)
        self.file.setText("Изменить..")
        self.delete.clicked.connect(self.deleteFile)

    def deleteFile(self):
        self.fname = ""
        self.label_file.setText(" ")

    def insert(self):
        atc = self.atc.currentText()
        surname = self.surname.text()
        name = self.name.text()
        middlename = self.middlename.text()
        address = self.address.text()
        number = self.number.text()
        position = self.position.currentText()
        benefit = self.benefit.currentText()
        document = self.fname

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
            elif benefit_id is None and len(self.fname) > 2:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Выберите тип льготы или удалите фото льготы!"),
                                                  QMessageBox.Ok)
            elif benefit_id is not None and len(self.fname) < 2:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Добавьте фото льготы или уберите льготу!"),
                                                  QMessageBox.Ok)
            elif len(number) != 13:
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Номер телефона не может быть больше или меньше 13 символов!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            else:
                self.query.prepare(
                    "INSERT INTO abonents(id_atc, surname, name, middlename, phone_number, address, id_position, id_benefit, document) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
                self.query.addBindValue(atc_id)
                self.query.addBindValue(surname)
                self.query.addBindValue(name)
                self.query.addBindValue(middlename)
                self.query.addBindValue(number)
                self.query.addBindValue(address)
                self.query.addBindValue(position_id)
                self.query.addBindValue(benefit_id)
                self.query.addBindValue(document)
                if not self.query.exec_():
                    messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                      self.tr("Абонент уже существует!"),
                                                      QMessageBox.Ok | QMessageBox.Cancel)
                else:
                    messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                         self.tr("Новая запись добавлена!"),
                                                         QMessageBox.Ok)
                    self.close()

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
