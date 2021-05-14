from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RefactorDialog(QDialog):
    customerAddedSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.data = None

        self.setWindowTitle("Добавление звонка")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label_capt = QLabel("Название льготы:")
        self.label_address = QLabel("Условия льготы:")
        self.label_district = QLabel("Тариф по льготе:")

        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.caption = QLineEdit()
        self.address = QLineEdit()
        self.caption.setMaxLength(15)
        self.address.setMaxLength(40)
        self.coeff = QDoubleSpinBox()

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
        self.gridlayout.addWidget(self.coeff, 6, 0)
        self.gridlayout.addWidget(self.buttonsBox, 8, 0)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)
        self.buttonsBox.rejected.connect(self.reject)

    def insert(self):
        name = self.caption.text()
        terms = self.address.text()
        spin = self.coeff.value()

        if not name or not terms or not spin or len(name) == 0 or len(terms) == 0:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Необходимо заполнить все поля формы!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        elif len(name) < 4 or len(terms) < 4:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Название льготы и условия льготы не могут быть меньше 4 символов!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        elif name.isdigit() or terms.isdigit():
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr(
                "Название льготы и условия льготы не могут состоять только из цифр!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        else:
            self.query.prepare(
                "INSERT INTO benefit(type, terms, tarriff) "
                "VALUES (?, ?, ?)")
            self.query.addBindValue(name)
            self.query.addBindValue(terms)
            self.query.addBindValue(spin)

            if not self.query.exec_():
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Звонок уже существует!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            else:
                messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                     self.tr("Новая запись добавлена!"),
                                                     QMessageBox.Ok)
                self.close()


