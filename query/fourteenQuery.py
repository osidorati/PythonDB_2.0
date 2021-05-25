from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class FourteenWidget(QWidget):
    customerAddedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.attempt = QSqlQueryModel(self)

        self.view = QTableView()
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        s = ("SELECT country.name_country, city.name_city, tariff.type_tariff, tariff.coefficient*country.price "
            " FROM tariff, city "
            " join country on country.id = city.id_country")
        self.attempt.setQuery(s)

        self.attempt.setHeaderData(0, Qt.Horizontal, "Название страны")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Название города")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Тариф")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Цена с учетом тарифа")

        self.label1 = QLabel("Вывод цен в городах с учетом тарифа: ")

        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)

        self.gridlayout.addWidget(self.label1, 1, 0, 1, 8)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)












