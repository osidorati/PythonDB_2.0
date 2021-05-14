from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ChangeDialog(QDialog):
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
        self.coeff = QDoubleSpinBox()

        self.save_btn = QPushButton("Сохранить изменения")
        self.cancel_btn = QPushButton("Cancel")

        self.gridlayout.addWidget(self.label_capt, 1, 0)
        self.gridlayout.addWidget(self.caption, 2, 0)
        self.gridlayout.addWidget(self.label_address, 3, 0)
        self.gridlayout.addWidget(self.address, 4, 0)
        self.gridlayout.addWidget(self.label_district, 5, 0)
        self.gridlayout.addWidget(self.coeff, 6, 0)
        self.gridlayout.addWidget(self.save_btn, 8, 0)
        self.gridlayout.addWidget(self.cancel_btn, 8, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.cancel)

    def cancel(self):
        self.close()

    def save(self):
        name = self.caption.text()
        terms = self.address.text()
        spin = self.coeff.value()

        if not name or not terms or not spin or len(name) == 0 or len(terms) == 0:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr("Необходимо заполнить все поля формы!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        elif len(name) < 4 or len(terms) < 4:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr(
                "Название льготы и условия льготы не могут быть меньше 4 символов!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        elif name.isdigit() or terms.isdigit():
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"), self.tr(
                "Название льготы и условия льготы не могут состоять только из цифр!"),
                                              QMessageBox.Ok | QMessageBox.Cancel)
        else:
            self.query.prepare(
                "update benefit set type = ?, terms = ?, tarriff = ? "
                "where id = ?")
            self.query.addBindValue(name)
            self.query.addBindValue(terms)
            self.query.addBindValue(spin)
            self.query.addBindValue(self.index)
            if not self.query.exec_():
                messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                                  self.tr("Запись уже существует!"),
                                                  QMessageBox.Ok | QMessageBox.Cancel)
            else:
                messageBox = QMessageBox.information(self, self.tr("Успех"),
                                                     self.tr("Запись изменена!"),
                                                     QMessageBox.Ok)
                self.close()

    def setIndex(self, index):
        self.index = index
        self.setData()

    def setData(self):
        query = QSqlQuery()
        data = []
        query.prepare("""select type, terms, tarriff from benefit where id = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(3):
                data.append(query.value(i))
        self.caption.setText(data[0])
        self.address.setText(data[1])
        self.coeff.setValue(data[2])
