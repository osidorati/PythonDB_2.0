from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class FourWidget(QWidget):
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
        self.attempt.setQuery("""SELECT city.id, city.name_city, country.price
                                from city join country on city.id_country = country.id""")

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_города")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Название города")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Цена 1 мин")

        self.view = QTableView()
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        self.label1 = QLabel("Цена 1 мин в городах:")
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label_count = QLabel("Количество записей: ")
        query = QSqlQuery()
        query.prepare("""select count(*) from city""")
        query.exec_()
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))

        self.label_count.setFont(font)
        self.gridlayout.addWidget(self.label1, 0, 2, 1, 8)
        self.gridlayout.addWidget(self.label_count, 2, 0)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)











