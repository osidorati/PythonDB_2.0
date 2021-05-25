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
        self.data = QDateEdit()

        self.label1 = QLabel("Название АТС:")
        self.label2 = QLabel("Район:")
        self.label3 = QLabel("Адрес:")
        self.label4 = QLabel("Дата основания:")
        self.label5 = QLabel("Статус АТС:")
        self.label6 = QLabel("Лицензия:")

        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")

        self.atc.setReadOnly(True)
        self.surname.setReadOnly(True)
        self.name.setReadOnly(True)
        self.middlename.setReadOnly(True)
        self.number.setReadOnly(True)
        self.address.setReadOnly(True)
        self.data.setReadOnly(True)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok
        )

        self.gridlayout.addWidget(self.label1, 1, 0)
        self.gridlayout.addWidget(self.label2, 2, 0)
        self.gridlayout.addWidget(self.label3, 3, 0)
        self.gridlayout.addWidget(self.label4, 4, 0)
        self.gridlayout.addWidget(self.label5, 5, 0)
        self.gridlayout.addWidget(self.label6, 6, 0)

        self.gridlayout.addWidget(self.atc, 1, 1)
        self.gridlayout.addWidget(self.surname, 2, 1)
        self.gridlayout.addWidget(self.name, 3, 1)
        self.gridlayout.addWidget(self.data, 4, 1)
        self.gridlayout.addWidget(self.number, 5, 1)
        self.gridlayout.addWidget(self.address, 6, 1)

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
        query.prepare("""select atc.caption, district.name_district, atc.address, 
                                    atc.year, atc.atc_state, atc.license 
                                    from atc join district on atc.id_district = district.id where atc.id_atc = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(6):
                data.append(query.value(i))
        self.atc.setReadOnly(True)
        self.atc.setText(data[0])
        self.surname.setText(data[1])
        self.name.setText(data[2])
        self.data.setDate(data[3])
        self.number.setText(str(data[4]))
        self.address.setText(data[5])




