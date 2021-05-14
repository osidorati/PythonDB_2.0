from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class LookDialog(QDialog):
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

        self.atc = QLineEdit()
        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.middlename = QLineEdit()
        self.number = QLineEdit()
        self.address = QLineEdit()
        self.position = QLineEdit()
        self.benefit = QLineEdit()

        self.label = QLabel("Сведения об абоненте:")
        self.label1 = QLabel("Фамилия:")
        self.label2 = QLabel("Имя:")
        self.label3 = QLabel("Отчество:")
        self.label4 = QLabel("Номер телефона:")
        self.label5 = QLabel("Номер телефона собеседника:")
        self.label6 = QLabel("Продолжительность:")
        self.label7 = QLabel("Город:")
        self.label8 = QLabel("Тариф:")
        self.label9 = QLabel("Дата:")

        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.middlename = QLineEdit()
        self.number = QLineEdit()
        self.number_in = QLineEdit()
        self.duration = QLineEdit()
        self.date = QDateEdit()
        self.tariff = QLineEdit()
        self.city = QLineEdit()

        self.surname.setReadOnly(True)
        self.name.setReadOnly(True)
        self.middlename.setReadOnly(True)
        self.number.setReadOnly(True)
        self.number_in.setReadOnly(True)
        self.duration.setReadOnly(True)
        self.date.setReadOnly(True)
        self.tariff.setReadOnly(True)
        self.city.setReadOnly(True)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok
        )

        self.gridlayout.addWidget(self.label, 1, 0)
        self.gridlayout.addWidget(self.label1, 2, 0)
        self.gridlayout.addWidget(self.label2, 3, 0)
        self.gridlayout.addWidget(self.label3, 4, 0)
        self.gridlayout.addWidget(self.label7, 5, 0)
        self.gridlayout.addWidget(self.label4, 6, 0)
        self.gridlayout.addWidget(self.label5, 7, 0)
        self.gridlayout.addWidget(self.label6, 8, 0)
        self.gridlayout.addWidget(self.label8, 9, 0)
        self.gridlayout.addWidget(self.label9, 10, 0)

        self.gridlayout.addWidget(self.surname, 2, 1)
        self.gridlayout.addWidget(self.name, 3, 1)
        self.gridlayout.addWidget(self.middlename, 4, 1)
        self.gridlayout.addWidget(self.city, 5, 1)
        self.gridlayout.addWidget(self.number, 6, 1)
        self.gridlayout.addWidget(self.number_in, 7, 1)
        self.gridlayout.addWidget(self.duration, 8, 1)
        self.gridlayout.addWidget(self.date, 10, 1)
        self.gridlayout.addWidget(self.tariff, 9, 1)
        self.gridlayout.addWidget(self.buttonsBox, 12, 0, 1, 2)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.insert)

    def insert(self):
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
        print(data)
        self.surname.setText(data[0])
        self.name.setText(data[1])
        self.middlename.setText(data[2])
        self.city.setText(data[4])
        self.number.setText(data[3])
        self.number_in.setText(data[5])
        self.tariff.setText(data[8])
        self.duration.setText(str(data[7]))
        self.date.setDate(data[6])





