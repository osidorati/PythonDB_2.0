from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class LookDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.data = None

        self.setWindowTitle("Добавление района")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label_distr = QLabel("Название города:")
        self.label_country = QLabel("Cтранa:")
        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")
        self.name_district_add = QLineEdit()
        self.country = QLineEdit()
        self.name_district_add.setReadOnly(True)
        self.country.setReadOnly(True)

        self.cancel_btn = QPushButton("Ok")

        self.gridlayout.addWidget(self.country, 1, 0)
        self.gridlayout.addWidget(self.label_country, 0, 0)
        self.gridlayout.addWidget(self.label_distr, 2, 0)
        self.gridlayout.addWidget(self.name_district_add, 3, 0)
        self.gridlayout.addWidget(self.cancel_btn, 12, 0)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.cancel_btn.clicked.connect(self.cancel)

    def cancel(self):
        self.close()

    def setIndex(self, index):
        self.index = index
        self.setData()

    def setData(self):
        query = QSqlQuery()
        data = []
        query.prepare("select country.name_country, city.name_city "
                    "from city join country on city.id_country = country.id where city.id = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(2):
                data.append(query.value(i))
        self.country.setText(data[0])
        self.name_district_add.setText(data[1])
