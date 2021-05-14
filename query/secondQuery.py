from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class SecondWidget(QWidget):
    customerAddedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.attempt = QSqlQueryModel(self)
        self.attempt.setQuery("""select atc.id_atc, atc.caption, district.name_district, atc.address, 
                                    atc.year, atc.atc_state, atc.license 
                                    from atc join district on atc.id_district = district.id;""")

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_АТС")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Название АТС")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Район")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Адрес")
        self.attempt.setHeaderData(4, Qt.Horizontal, "Год открытия")
        self.attempt.setHeaderData(5, Qt.Horizontal, "Тип собственности")
        self.attempt.setHeaderData(6, Qt.Horizontal, "Лицензия")

        self.view = QTableView()
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)
        self.box = QComboBox()

        district = []
        self.query = QSqlQuery()
        self.query.exec("""SELECT name_district FROM district""")
        while self.query.next():
            district.append(str(self.query.value(0)))
        self.box.addItems(district)

        self.btn = QPushButton("Вывести")
        self.btn.setFixedWidth(100)

        self.label1 = QLabel("Количеcтво АТС в указанном районе:")
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.gridlayout.addWidget(self.label1, 0, 2, 1, 8)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)
        self.gridlayout.addWidget(self.box, 1, 2)
        self.gridlayout.addWidget(self.btn, 1, 6)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        self.btn.clicked.connect(self.update)

    def update(self):
        district = self.box.currentText()
        s = ("select atc.id_atc, atc.caption, district.name_district, atc.address, atc.year, atc.atc_state, atc.license "
            " from atc join district on atc.id_district = district.id "
            " where district.name_district = '" + district + "'")
        self.attempt.setQuery(s)








