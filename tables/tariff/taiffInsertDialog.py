from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RefactorDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.data = None
        self.query = QSqlQuery()
        self.setWindowTitle("Добавление района")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label_distr = QLabel("Название тарифа:")
        self.label2 = QLabel("Время начала:")
        self.label3 = QLabel("Время конца:")
        self.label4 = QLabel("Коэффициент:")
        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")
        self.name_district_add = QLineEdit()
        self.date1 = QTimeEdit()
        self.date2 = QTimeEdit()
        self.spin = QDoubleSpinBox()

        rx = QRegExp("[а-яА-Яa-zA-Z]+")
        validator = QRegExpValidator(rx, self)
        self.name_district_add.setValidator(validator)
        self.name_district_add.setMaxLength(20)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.gridlayout.addWidget(self.buttonsBox, 7, 0)
        self.gridlayout.addWidget(self.name_district_add, 1, 0, 1, 2)
        self.gridlayout.addWidget(self.label_distr, 0, 0)
        self.gridlayout.addWidget(self.label2, 2, 0)
        self.gridlayout.addWidget(self.date1, 2, 1)
        self.gridlayout.addWidget(self.label3, 4, 0)
        self.gridlayout.addWidget(self.date2, 4, 1)
        self.gridlayout.addWidget(self.label4, 5, 0)
        self.gridlayout.addWidget(self.spin, 5, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)
        self.buttonsBox.rejected.connect(self.reject)

    def insert(self):
        name = self.name_district_add.text()
        data1 = self.date1.text()
        data2 = self.date2.text()
        spin = self.spin.value()

        if not name or len(name) == 0:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Необходимо заполнить все поля формы!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        elif len(name) < 3:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Название тарифа не может быть меньше 3 символов!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        else:
            self.query.prepare(
                "INSERT INTO tariff(type_tariff, time_start, time_finish, coefficient) "
                "VALUES (?, ?, ?, ?)")
            self.query.addBindValue(name)
            self.query.addBindValue(data1)
            self.query.addBindValue(data2)
            self.query.addBindValue(spin)
            if not self.query.exec_():
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Тариф уже существует!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            else:
                messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                     self.tr("Новая запись добавлена!"),
                                                     QMessageBox.Ok)
                self.close()



